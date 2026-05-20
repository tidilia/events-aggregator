from urllib.parse import urljoin

import httpx


class CapashinoClient:
    def __init__(self, base_url: str, api_key: str, http_client: httpx.AsyncClient):
        self.base_url = base_url
        self.api_key = api_key
        self.http_client = http_client

    async def send_notification(self, ticket_id: str, ticket_information: dict):
        message = f"{ticket_information['first_name']} {ticket_information['last_name']}, you're successfully registered for event with seat {ticket_information['seat']}"
        payload = {
            "message": message,
            "reference_id": ticket_id,
            "idempotency_key": ticket_id,
        }

        headers = {"X-API-Key": self.api_key, "Content-Type": "application/json"}

        async with httpx.AsyncClient() as client:
            response = await client.post(
                urljoin(self.base_url, "/api/notifications"),
                json=payload,
                headers=headers,
            )

        response.raise_for_status()
        return response.json()
