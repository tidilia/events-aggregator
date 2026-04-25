class EventsPaginator:
    def __init__(self, client, changed_at: str):
        self.client = client
        self.changed_at = changed_at
        self.cursor = None
        self.has_more = True
        self.buffer = []

    def __aiter__(self):
        return self

    async def __anext__(self):
        if not self.buffer and not self.has_more:
            raise StopAsyncIteration

        if not self.buffer:
            response = await self.client.events(
                changed_at=self.changed_at,
                cursor=self.cursor
            )

            self.buffer = response["results"]
            self.cursor = response.get("next_cursor")
            self.has_more = self.cursor is not None

        if not self.buffer:
            raise StopAsyncIteration

        return self.buffer.pop(0)