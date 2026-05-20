from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.outbox import Outbox
from app.models.ticket import Ticket


class TicketsRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save_ticket(self, ticket_data: dict, outbox_data: dict):
        ticket = Ticket(**ticket_data)
        outbox = Outbox(**outbox_data)
        self.session.add(ticket)
        await self.session.flush()
        self.session.add(outbox)
        await self.session.commit()

    async def get(self, ticket_id: str) -> Ticket | None:
        result = await self.session.get(Ticket, ticket_id)
        return result

    async def delete(self, ticket_id: str):
        ticket = await self.get(ticket_id)
        if ticket:
            await self.session.delete(ticket)
            await self.session.commit()

    async def get_by_idempotency_key_with_user(self, key: str):
        result = await self.session.execute(
            select(Ticket)
            .options(selectinload(Ticket.user))
            .where(Ticket.idempotency_key == key)
        )

        return result.scalar_one_or_none()
