from app.services.seats_cache import seats_cache
from app.models.enums import EventStatus
from app.exceptions import EventNotFoundError, EventNotPublishedError

class SeatsService:
    def __init__(self, repo, client):
        self.repo = repo
        self.client = client

    async def get_seats(self, event_id: str):
        event = await self.repo.get_event_by_id(event_id)
        
        if not event:
            raise EventNotFoundError(event_id)
        
        if event.status != EventStatus.published:
            raise EventNotPublishedError
        
        cached = seats_cache.get(event_id)
        if cached:
            return ({"event_id": event_id, "available_seats": cached})

        data = await self.client.event_seats(event_id)
        result = {"event_id": event_id, "available_seats": data}
        seats_cache.set(event_id, data, ttl=30)
        return result