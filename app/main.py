import asyncio
import sentry_sdk
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sentry_sdk.integrations.fastapi import FastApiIntegration

from app.api.router import api_router
from app.config import EVENTS_PROVIDER_URL, LMS_API_KEY, CAPASHINO_URL, SENTRY_DSN

from app.clients.events_provider import EventsProviderClient
from app.sync.worker import sync_loop

import httpx

from app.workers.outbox import outbox_worker
from app.clients.capashino import CapashinoClient

sentry_sdk.init(
    dsn=SENTRY_DSN,
    integrations=[FastApiIntegration()],
    traces_sample_rate=1.0,
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    base_url = EVENTS_PROVIDER_URL
    capashino_url = CAPASHINO_URL

    api_key = LMS_API_KEY
    
    client = EventsProviderClient(
        base_url=base_url, api_key=api_key, http_client=httpx.AsyncClient())
    capashino_client = CapashinoClient(
        base_url=capashino_url, api_key=api_key, http_client=httpx.AsyncClient()
    )
    
    sync_task = asyncio.create_task(
        sync_loop(client)
    )
    outbox_task = asyncio.create_task(
        outbox_worker(capashino_client)
    )

    try:
        yield
    finally:
        sync_task.cancel()
        outbox_task.cancel()


app = FastAPI(lifespan=lifespan)

app.include_router(api_router, prefix="/api")

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    if request.url.path.startswith("/api/tickets"):
        return JSONResponse(
            status_code=400,
            content={"detail": exc.errors()},
        )

    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()},
    )