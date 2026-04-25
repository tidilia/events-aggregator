class SyncUsecase:
    def __init__(self, sync_service):
        self.sync_service = sync_service

    async def trigger(self):
        await self.sync_service.sync_once()
