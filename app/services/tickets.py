from fastapi import HTTPException
from datetime import datetime, timezone

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
            raise HTTPException(status_code=404, detail="Event not found")
        
        if event.status != "published":
            raise HTTPException(status_code=400, detail="Event is not published")

        
        if event.registration_deadline < datetime.now(timezone.utc):
            raise HTTPException(status_code=400, detail="Registration deadline has passed")

        
        seats = await self.seats_service.get_seats(event_id)
        if data.seat not in seats["available_seats"]:
            raise HTTPException(status_code=400, detail="Seat is not available")
        
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

        await self.tickets_repo.save_ticket(ticket_data)

        return result
    
    async def unregister(self, ticket_id: str):
        ticket = await self.tickets_repo.get(ticket_id)

        if not ticket:
            raise HTTPException(status_code=404, detail="Ticket not found")

        await self.client.unregister(ticket.event_id, ticket_id)
        await self.tickets_repo.delete(ticket_id)
        
        return {"success": True}
