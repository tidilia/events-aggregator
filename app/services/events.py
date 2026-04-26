from fastapi import HTTPException

class EventsService:
    def __init__(self, repo):
        self.repo = repo

    async def get_events(self, date_from, page, page_size):
        offset = (page - 1) * page_size

        events = await self.repo.get_events(
            date_from=date_from,
            limit=page_size,
            offset=offset
        )

        total = await self.repo.count_events(date_from)

        return events, total
    
    async def get_event(self, event_id: str):
        event = await self.repo.get_event_by_id(event_id)

        if not event:
            raise HTTPException(status_code=404, detail="Event not found")

        return event