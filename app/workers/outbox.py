import asyncio

from app.repositories.outbox import OutboxRepository
from app.clients.capashino import CapashinoClient


POLL_INTERVAL = 5  


async def outbox_worker(
    outbox_repo: OutboxRepository,
    capashino_client: CapashinoClient,
):
    while True:
        try:
            outbox_events = await outbox_repo.get_pending()

            for event in outbox_events:
                try:
                    await capashino_client.send_notification(event.ticket_id, event.payload)
                    await outbox_repo.mark_sent(event.id)

                except Exception as e:
                    print(f"[Outbox] failed event {event.id}: {e}")

            await asyncio.sleep(POLL_INTERVAL)

        except Exception as e:
            print(f"[Outbox worker crash]: {e}")
            await asyncio.sleep(POLL_INTERVAL)