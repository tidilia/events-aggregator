from datetime import datetime
from app.sync.paginator import EventsPaginator


async def sync_events(client, events_repo, sync_repo):
    last_changed_at = await sync_repo.get_last_changed_at()

    # 1. первая синхронизация
    if not last_changed_at:
        changed_at = "2000-01-01"
        max_changed_at = None
    else:
        changed_at = last_changed_at.strftime("%Y-%m-%d")
        max_changed_at = last_changed_at

    paginator = EventsPaginator(client, changed_at)

    async for event in paginator:
        await events_repo.upsert_event(event)

        event_dt = datetime.fromisoformat(event["changed_at"])

        if max_changed_at is None or event_dt > max_changed_at:
            max_changed_at = event_dt

    # 2. обновляем метаданные
    if max_changed_at:
        await sync_repo.update_sync_metadata(
            last_changed_at=max_changed_at,
            sync_time=datetime.utcnow()
        )