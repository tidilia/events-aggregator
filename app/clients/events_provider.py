import httpx


class EventsProviderClient:
    def __init__(self, base_url: str, api_key: str, http_client: httpx.AsyncClient):
        self.base_url = base_url
        self.api_key = api_key
        self.http_client = http_client

    async def events(self, changed_at: str, cursor: str | None = None):
        params = {
            "changed_at": changed_at
        }

        if cursor:
            params["cursor"] = cursor

        headers = {
            "x-api-key": self.api_key
        }

        response = await self.http_client.get(
            self.base_url,
            params=params,
            headers=headers
        )

        response.raise_for_status()
        return response.json()
    

    async def event_seats(self, event_id: str):
        headers = {
                "x-api-key": self.api_key
            }
    
        response = await self.http_client.get(
            f"{self.base_url}{event_id}/seats/",
            headers=headers
        )
        response.raise_for_status()
        
        result = response.json()
        return result.get("seats")
    
    async def register(self, event_id: str, payload: dict):
        headers = {
                "x-api-key": self.api_key
            }
    
        response = await self.http_client.post(
            f"{self.base_url}{event_id}/register/",
            json=payload,
            headers=headers
        )
        response.raise_for_status()
        
        return response.json()
    
    async def unregister(self, event_id: str, ticket_id: str):
        await self.http_client.request(
            "DELETE",
            f"{self.base_url}{event_id}/unregister/",
            json={"ticket_id": ticket_id},
            headers={"x-api-key": self.api_key}
        )