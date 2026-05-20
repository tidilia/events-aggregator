from app.metrics import (events_total, tickets_cancelled_total,
                         tickets_created_total)


class MetricsService:

    def __init__(self, tickets_repo, events_repo):
        self.tickets_repo = tickets_repo
        self.events_repo = events_repo

    async def update_business_metrics(self):
        tickets_created_total.set(await self.tickets_repo.count_all())

        tickets_cancelled_total.set(await self.tickets_repo.count_cancelled())

        events_total.set(await self.events_repo.count_all())
