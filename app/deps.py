from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.clients.events_provider import EventsProviderClient
from app.repositories.events import EventsRepository
from app.repositories.sync import SyncRepository
from app.sync.sync_service import SyncService, sync_events
from app.usecases.sync import SyncUsecase


def get_events_client() -> EventsProviderClient:
    return EventsProviderClient()


def get_events_repository(
    db: AsyncSession = Depends(get_db),
) -> EventsRepository:
    return EventsRepository(db)


def get_sync_repository(
    db: AsyncSession = Depends(get_db),
) -> SyncRepository:
    return SyncRepository(db)


def get_sync_service(
    client: EventsProviderClient = Depends(get_events_client),
    events_repo: EventsRepository = Depends(get_events_repository),
    sync_repo: SyncRepository = Depends(get_sync_repository),
) -> SyncService:
    return SyncService(
        client=client,
        repo=events_repo,
        sync_fn=lambda client, repo: sync_events(client, repo, sync_repo),
    )


def get_sync_usecase(
    sync_service: SyncService = Depends(get_sync_service),
) -> SyncUsecase:
    return SyncUsecase(sync_service)