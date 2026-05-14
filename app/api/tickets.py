from fastapi import APIRouter, Depends, status, HTTPException
from app.schemas.event import RegisterRequest, RegisterResponse
from app.deps import get_tickets_service
from app.services.tickets import TicketsService
from app.exceptions import EventNotFoundError, EventNotPublishedError, RegistrationDeadlinePassedError, SeatNotAvailableError, TicketNotFoundError, IdempotencyConflictError

router = APIRouter()

@router.post("/tickets", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED)
async def create_ticket(
    payload: RegisterRequest,
    service: TicketsService = Depends(get_tickets_service)
):
    try:
        result = await service.register(payload)
        return result
    except (EventNotPublishedError, RegistrationDeadlinePassedError, SeatNotAvailableError) as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except EventNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    except IdempotencyConflictError as e:
        raise HTTPException(status_code=409, detail=str(e)) from e

@router.delete("/tickets/{ticket_id}", status_code=status.HTTP_200_OK)
async def delete_ticket(
    ticket_id: str,
    service: TicketsService = Depends(get_tickets_service)
):
    try:
        result = await service.unregister(ticket_id)
        return result 
    except TicketNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e