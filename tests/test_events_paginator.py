import pytest

from app.sync.paginator import EventsPaginator


class MockClient:
    def __init__(self):
        self.calls = 0

    async def events(self, changed_at, cursor=None):
        self.calls += 1

        if self.calls == 1:
            return {
                "results": [{"id": "1"}, {"id": "2"}],
                "next_cursor": "abc",
            }

        return {
            "results": [{"id": "3"}],
            "next_cursor": None,
        }


@pytest.mark.asyncio
async def test_events_paginator_iteration():
    client = MockClient()

    paginator = EventsPaginator(client, changed_at="2000-01-01")

    results = []

    async for event in paginator:
        results.append(event)

    assert len(results) == 3
    assert client.calls == 2
