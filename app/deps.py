import os
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.clients.events_provider import EventsProviderClient
from app.repositories.events import EventsRepository
from app.repositories.sync import SyncRepository
from app.repositories.tickets import TicketsRepository
from app.repositories.users import UsersRepository
from app.services.events import EventsService
from app.services.tickets import TicketsService
from app.services.seats import SeatsService
from app.sync.sync_service import SyncService, sync_events
from app.usecases.sync import SyncUsecase
from httpx import AsyncClient

base_url=os.getenv("EVENTS_PROVIDER_URL")
api_key =os.getenv("LMS_API_KEY")

def get_events_client() -> EventsProviderClient:
    return EventsProviderClient(
        base_url=base_url,
        api_key=api_key,
        http_client=AsyncClient(),
    )


def get_events_repository(
    db: AsyncSession = Depends(get_db),
) -> EventsRepository:
    return EventsRepository(db)


def get_sync_repository(
    db: AsyncSession = Depends(get_db),
) -> SyncRepository:
    return SyncRepository(db)

def get_tickets_repository(
    db: AsyncSession = Depends(get_db),
) -> TicketsRepository:
    return TicketsRepository(db)

def get_users_repository(
    db: AsyncSession = Depends(get_db),
) -> UsersRepository:
    return UsersRepository(db)


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


def get_events_repo(
    session: AsyncSession = Depends(get_db)
) -> EventsRepository:
    return EventsRepository(session)

def get_seats_service(
    repo: EventsRepository = Depends(get_events_repo),
    client: EventsProviderClient = Depends(get_events_client)
) -> SeatsService:
    return SeatsService(repo, client)

def get_events_service(
    repo: EventsRepository = Depends(get_events_repo),
) -> EventsService:
    return EventsService(repo)

def get_tickets_service(
    events_repo: EventsRepository = Depends(get_events_repo),
    client: EventsProviderClient = Depends(get_events_client),
    seats_service: SeatsService = Depends(get_seats_service),
    users_repo: UsersRepository = Depends(get_users_repository),
    tickets_repo: TicketsRepository = Depends(get_tickets_repository)
) -> TicketsService:
    return TicketsService(seats_service, client, events_repo, users_repo, tickets_repo)