from datetime import datetime, timezone
from uuid import uuid4
from app.models.enums import EventStatus
from app.exceptions import EventNotFoundError, EventNotPublishedError, RegistrationDeadlinePassedError, SeatNotAvailableError, TicketNotFoundError  

class TicketsService:
    def __init__(self, seats_service, client, events_repo, users_repo, tickets_repo):
        self.seats_service = seats_service
        self.client = client
        self.repo = events_repo
        self.users_repo = users_repo
        self.tickets_repo = tickets_repo

    async def get_or_create_user(self, data):
        user = await self.users_repo.get_by_email(data.email)
        if not user:
            user_data = {
                "first_name": data.first_name,
                "last_name": data.last_name,
                "email": data.email
            }
            user = await self.users_repo.create(user_data)
        return user

    async def register(self, data):
        event_id = data.event_id
        event = await self.repo.get_event_by_id(event_id)
        user = await self.get_or_create_user(data)

        if not event:
            raise EventNotFoundError(event_id)
        
        if event.status != EventStatus.published:
            raise EventNotPublishedError

        
        if event.registration_deadline < datetime.now(timezone.utc):
            raise RegistrationDeadlinePassedError

        
        seats = await self.seats_service.get_seats(event_id)
        if data.seat not in seats["available_seats"]:
            raise SeatNotAvailableError
        
        payload = {
            "first_name": data.first_name,
            "last_name": data.last_name,
            "seat": data.seat,
            "email": data.email
        }
        
        result = await self.client.register(event_id, payload)
        
        ticket_data = {
            "id": result["ticket_id"],
            "event_id": event_id,
            "user_id": user.id,
            "seat": data.seat,
            "created_at": datetime.now(timezone.utc)
        }
        
        outbox_data = {
            "id": str(uuid4()),
            "payload": payload,
            "ticket_id": ticket_data["id"],
            "created_at": ticket_data["created_at"]
        }

        await self.tickets_repo.save_ticket(ticket_data, outbox_data)

        return result
    
    async def unregister(self, ticket_id: str):
        ticket = await self.tickets_repo.get(ticket_id)

        if not ticket:
            raise TicketNotFoundError(ticket_id)

        await self.client.unregister(ticket.event_id, ticket_id)
        await self.tickets_repo.delete(ticket_id)
        
        return {"success": True}
