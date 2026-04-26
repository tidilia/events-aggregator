from fastapi import APIRouter
from app.api import health, sync, events, tickets

api_router = APIRouter()

api_router.include_router(health.router)
api_router.include_router(sync.router)
api_router.include_router(events.router)
api_router.include_router(tickets.router)

