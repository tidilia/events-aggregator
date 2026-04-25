from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.sync import SyncMetadata
from datetime import datetime


class SyncRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_last_changed_at(self) -> datetime | None:
        result = await self.session.execute(
            select(SyncMetadata)
            .order_by(SyncMetadata.id.desc())
            .limit(1)
        )

        row = result.scalar_one_or_none()
        return row.last_changed_at if row else None

    async def update_sync_metadata(
        self,
        last_changed_at: datetime,
        sync_time: datetime,
        status: str = "success"
    ):
        record = SyncMetadata(
            last_changed_at=last_changed_at,
            last_sync_time=sync_time,
            sync_status=status
        )

        self.session.add(record)
        await self.session.commit()
