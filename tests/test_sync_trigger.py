import pytest
from unittest.mock import AsyncMock
from httpx import AsyncClient, ASGITransport

from app.main import app
from app.deps import get_sync_usecase


@pytest.mark.asyncio
async def test_manual_sync_trigger():
    mock_usecase = AsyncMock()
    mock_usecase.trigger.return_value = None

    app.dependency_overrides[get_sync_usecase] = lambda: mock_usecase

    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/api/sync/trigger")

    assert response.status_code == 200
    mock_usecase.trigger.assert_called_once()

    app.dependency_overrides.clear()
