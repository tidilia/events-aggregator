from fastapi import APIRouter, Query, Request, Depends
from datetime import datetime
from app.schemas.event import EventsListResponse
from app.utils.pagination import build_url
from app.deps import get_events_service, get_seats_service
from app.services.events import EventsService
from app.services.seats import SeatsService


router = APIRouter()


@router.get("/events", response_model=EventsListResponse)
async def get_events(
    request: Request,
    date_from: str | None = Query(None),
    page: int = 1,
    page_size: int = 20,
    service: EventsService = Depends(get_events_service)
):
    parsed_date = datetime.fromisoformat(date_from) if date_from else None

    events, total = await service.get_events(
        date_from=parsed_date,
        page=page,
        page_size=page_size
    )

    base_url = str(request.base_url).rstrip("/") + "/api/events"

    next_url = None
    prev_url = None

    if page * page_size < total:
        next_url = build_url(base_url, page + 1, page_size, date_from)

    if page > 1:
        prev_url = build_url(base_url, page - 1, page_size, date_from)
        
    print(prev_url)
    print(page)

    return {
        "count": total,
        "next": next_url,
        "previous": prev_url,
        "results": [
            {
                "id": e.id,
                "name": e.name,
                "place": {
                    "id": e.place_id,
                    "name": e.place_name,
                    "city": e.place_city,
                    "address": e.place_address,
                },
                "event_time": e.event_time,
                "registration_deadline": e.registration_deadline,
                "status": e.status,
                "number_of_visitors": e.number_of_visitors,
            }
            for e in events
        ]
    }
    
@router.get("/events/{event_id}/seats")
async def get_event_seats(
    event_id: str,
    service: SeatsService = Depends(get_seats_service)
):
    return await service.get_seats(event_id)


@router.get("/events/{event_id}")
async def get_event(
    event_id: str,
    service: EventsService = Depends(get_events_service)
):
    event = await service.get_event(event_id)

    return {
        "id": event.id,
        "name": event.name,
        "place": {
            "id": event.place_id,
            "name": event.place_name,
            "city": event.place_city,
            "address": event.place_address,
            "seats_pattern": event.place_seats_pattern,
        },
        "event_time": event.event_time,
        "registration_deadline": event.registration_deadline,
        "status": event.status,
        "number_of_visitors": event.number_of_visitors,
    }
    