import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.router import api_router

from app.db.session import SessionLocal
from app.clients.events_provider import EventsProviderClient
from app.repositories.events import EventsRepository
from app.repositories.sync import SyncRepository
from app.sync.worker import sync_loop

import os
import httpx


@asynccontextmanager
async def lifespan(app: FastAPI):
    session = SessionLocal()

    events_repo = EventsRepository(session)
    sync_repo = SyncRepository(session)

    base_url = os.getenv(
        "EVENTS_PROVIDER_URL",
        "https://events-provider.dev-2.python-labs.ru/api/events/"
    )

    api_key = os.getenv("LMS_API_KEY")

    client = EventsProviderClient(
        base_url=base_url, api_key=api_key, http_client=httpx.AsyncClient())

    task = asyncio.create_task(
        sync_loop(client, events_repo, sync_repo)
    )

    try:
        yield
    finally:
        task.cancel()

        await session.close()


app = FastAPI(lifespan=lifespan)

app.include_router(api_router, prefix="/api")
