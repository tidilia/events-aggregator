from fastapi import APIRouter, Depends, status
from app.schemas.event import RegisterRequest, RegisterResponse
from app.deps import get_tickets_service
from app.services.tickets import TicketsService

router = APIRouter()

@router.post("/tickets", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED)
async def create_ticket(
    payload: RegisterRequest,
    service: TicketsService = Depends(get_tickets_service)
):
    result = await service.register(payload)
    return result

@router.delete("/tickets/{ticket_id}", status_code=status.HTTP_200_OK)
async def delete_ticket(
    ticket_id: str,
    service: TicketsService = Depends(get_tickets_service)
):
    result = await service.unregister(ticket_id)
    return result 