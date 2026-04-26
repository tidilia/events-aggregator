from fastapi import APIRouter, Depends
from app.schemas.event import RegisterRequest, RegisterResponse
from app.deps import get_tickets_service
from app.services.tickets import TicketsService

router = APIRouter()

@router.post("/tickets", response_model=RegisterResponse)
async def create_ticket(
    payload: RegisterRequest,
    service: TicketsService = Depends(get_tickets_service)
):
    result = await service.register(payload)
    return result

@router.delete("/tickets/{ticket_id}")
async def delete_ticket(
    ticket_id: str,
    service: TicketsService = Depends(get_tickets_service)
):
    result = await service.unregister(ticket_id)
    return result 