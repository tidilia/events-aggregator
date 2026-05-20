import asyncio

from app.sync.sync_service import sync_events
from app.unit_of_work import UnitOfWork


async def sync_loop(client):
    while True:
        uow = UnitOfWork()
        try:
            await sync_events(client, uow.events, uow.sync)
        except Exception as e:
            print("SYNC ERROR:", e)
        finally:
            await uow.close()

        await asyncio.sleep(60 * 60 * 24)
