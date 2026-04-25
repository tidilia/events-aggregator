import asyncio
from app.services.sync import sync_events


async def sync_loop(client, events_repo, sync_repo):
    while True:
        try:
            await sync_events(client, events_repo, sync_repo)
        except Exception as e:
            print("SYNC ERROR:", e)

        await asyncio.sleep(60 * 60 * 24)
