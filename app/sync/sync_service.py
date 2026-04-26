from datetime import datetime, timezone
from app.sync.paginator import EventsPaginator
from app.schemas.event import EventSchema
class SyncService:
    def __init__(self, client, repo, sync_fn):
        self.client = client
        self.repo = repo
        self.sync_fn = sync_fn

    async def sync_once(self):
        await self.sync_fn(self.client, self.repo)


async def sync_events(client, events_repo, sync_repo):
    last_changed_at = await sync_repo.get_last_changed_at()

    if not last_changed_at:
        changed_at = datetime(2000, 1, 1, tzinfo=timezone.utc)
        max_changed_at = None
    else:
        changed_at = last_changed_at
        max_changed_at = last_changed_at

    paginator = EventsPaginator(client, changed_at)
    

    async for raw_event in paginator:
        event = EventSchema.model_validate(raw_event)
        await events_repo.upsert_event(event)

        event_dt = event.changed_at

        if max_changed_at is None or event_dt > max_changed_at:
            max_changed_at = event_dt

    # 2. обновляем метаданные
    if max_changed_at:
        await sync_repo.update_sync_metadata(
            last_changed_at=max_changed_at,
            sync_time=datetime.utcnow()
        )
