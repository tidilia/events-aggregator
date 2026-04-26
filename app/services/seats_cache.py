import time

class SeatsCache:
    def __init__(self):
        self.storage = {}

    def get(self, event_id: str):
        data = self.storage.get(event_id)

        if not data:
            return None

        expires_at, value = data

        if time.time() > expires_at:
            del self.storage[event_id]
            return None

        return value

    def set(self, event_id: str, value, ttl: int = 30):
        expires_at = time.time() + ttl
        self.storage[event_id] = (expires_at, value)


seats_cache = SeatsCache()