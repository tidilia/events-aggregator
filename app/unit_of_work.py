from app.db.session import SessionLocal
from app.repositories.events import EventsRepository
from app.repositories.sync import SyncRepository
from app.repositories.outbox import OutboxRepository


class UnitOfWork:
    def __init__(self):
        self.session = SessionLocal()

        self.events = EventsRepository(self.session)
        self.sync = SyncRepository(self.session)
        self.outbox = OutboxRepository(self.session)

    async def close(self):
        await self.session.close()