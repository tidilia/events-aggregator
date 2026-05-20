import time
from urllib.parse import urljoin

import httpx

from app.metrics import (events_provider_request_duration_seconds,
                         events_provider_requests_total)


class EventsProviderClient:
    def __init__(self, base_url: str, api_key: str, http_client: httpx.AsyncClient):
        self.base_url = base_url
        self.api_key = api_key
        self.http_client = http_client

    async def _request(self, method: str, url: str, endpoint_label: str, **kwargs):
        start = time.time()
        status = "error"

        try:
            response = await self.http_client.request(method, url, **kwargs)
            status = str(response.status_code)

            response.raise_for_status()
            return response

        except Exception:
            raise

        finally:
            duration = time.time() - start

            events_provider_request_duration_seconds.labels(
                endpoint=endpoint_label
            ).observe(duration)

            events_provider_requests_total.labels(
                endpoint=endpoint_label,
                status=status,
            ).inc()

    async def events(self, changed_at: str, cursor: str | None = None):
        params = {"changed_at": changed_at}

        if cursor:
            params["cursor"] = cursor

        headers = {"x-api-key": self.api_key}

        response = await self._request(
            "GET",
            self.base_url,
            endpoint_label="/events",
            params=params,
            headers=headers,
        )
        return response.json()

    async def event_seats(self, event_id: str):
        headers = {"x-api-key": self.api_key}

        response = await self._request(
            "GET",
            urljoin(self.base_url, f"{event_id}/seats/"),
            endpoint_label="/seats",
            headers=headers,
        )

        return response.json().get("seats")

    async def register(self, event_id: str, payload: dict):
        headers = {"x-api-key": self.api_key}

        try:
            response = await self._request(
                "POST",
                urljoin(self.base_url, f"{event_id}/register/"),
                endpoint_label="/registration",
                json=payload,
                headers=headers,
            )
            return response.json()
        except httpx.HTTPStatusError as e:
            print("EVENTS PROVIDER ERROR:", e.response.text)
            raise

        except httpx.RequestError as e:
            print("NETWORK ERROR:", str(e))
            raise

    async def unregister(self, event_id: str, ticket_id: str):
        await self.http_client.request(
            "DELETE",
            urljoin(self.base_url, f"{event_id}/unregister/"),
            json={"ticket_id": ticket_id},
            headers={"x-api-key": self.api_key},
        )
