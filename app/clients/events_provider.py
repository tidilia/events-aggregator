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
        
        print("STATUS:", response.status_code)

        if response.status_code != 200:
            print("ERROR BODY:", await response.text())

        response.raise_for_status()
        return response.json()