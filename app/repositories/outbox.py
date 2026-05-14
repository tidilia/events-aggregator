from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.outbox import Outbox


class OutboxRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_pending(self, limit: int = 50):
        stmt = (
            select(Outbox)
            .where(Outbox.status == "pending")
            .order_by(Outbox.created_at)
            .with_for_update(skip_locked=True)
            .limit(limit)
        )

        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def mark_sent(self, outbox_id: str):
        stmt = (
            update(Outbox)
            .where(Outbox.id == outbox_id)
            .values(status="sent")
        )

        await self.session.execute(stmt)
        await self.session.commit()