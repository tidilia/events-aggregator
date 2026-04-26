from sqlalchemy.ext.asyncio import AsyncSession
from app.models.ticket import Ticket

class TicketsRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save_ticket(self, ticket_data: dict):
        ticket = Ticket(**ticket_data)
        self.session.add(ticket)
        await self.session.commit()
        
    async def get(self, ticket_id: str) -> Ticket | None:
        result = await self.session.get(Ticket, ticket_id)
        return result
    
    async def delete(self, ticket_id: str):
        ticket = await self.get(ticket_id)
        if ticket:
            await self.session.delete(ticket)
            await self.session.commit()