from app.sync.sync_service import SyncService
from app.sync.sync_service import sync_events


def get_sync_service(client, repo):
    return SyncService(client, repo, sync_events)
