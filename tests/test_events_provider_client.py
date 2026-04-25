import pytest
from unittest.mock import AsyncMock, MagicMock

from app.clients.events_provider import EventsProviderClient


@pytest.mark.asyncio
async def test_events_provider_client_events():
    mock_response = MagicMock()
    mock_response.raise_for_status = MagicMock()
    mock_response.json.return_value = {
        "results": [{"id": "1"}],
        "next": None,
    }

    mock_http = AsyncMock()
    mock_http.get.return_value = mock_response

    client = EventsProviderClient(
        base_url="http://test",
        api_key="test",
        http_client=mock_http,
    )

    result = await client.events(changed_at="2000-01-01")

    mock_http.get.assert_called_once()

    assert result == {
        "results": [{"id": "1"}],
        "next": None,
    }
