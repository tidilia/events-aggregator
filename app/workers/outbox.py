import asyncio
import traceback

from app.clients.capashino import CapashinoClient
from app.unit_of_work import UnitOfWork

POLL_INTERVAL = 5


async def outbox_worker(
    capashino_client: CapashinoClient,
):
    while True:
        uow = UnitOfWork()
        try:
            outbox_events = await uow.outbox.get_pending()

            for event in outbox_events:
                try:
                    await capashino_client.send_notification(
                        event.ticket_id, event.payload
                    )
                    await uow.outbox.mark_sent(event.id)

                except Exception as e:
                    print(f"[Outbox] failed event {event.id}: {repr(e)}")
                    print(traceback.format_exc())

            await asyncio.sleep(POLL_INTERVAL)

        except Exception as e:
            print(f"[Outbox worker crash]: {e}")
            await asyncio.sleep(POLL_INTERVAL)

        finally:
            await uow.close()
