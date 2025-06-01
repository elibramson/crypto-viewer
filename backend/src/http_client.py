from aiohttp import ClientSession

class HttpClient:
    def __init__(self, base_url: str, api_key: str):
        self.session = ClientSession(
            base_url=base_url,
            headers={
                "X-CMC_PRO_API_KEY": api_key,
            },
        )

class CoinMarketClient(HttpClient):
    async def get_listing(self):
        async with self.session.get("/v1/cryptocurrency/listings/latest") as response:
            result = await response.json()
            if response.status != 200:
                raise Exception(f"API Error: {result.get('status', {}).get('error_message', 'Unknown error')}")
            return result.get("data", [])
        
    async def get_currency_info(self, currency_id: int):
        async with self.session.get(
            "/v2/cryptocurrency/quotes/latest",
            params={"id": currency_id}
        ) as response:
            result = await response.json()
            if response.status != 200:
                raise Exception(f"API Error: {result.get('status', {}).get('error_message', 'Unknown error')}")
            return result.get("data", {}).get(str(currency_id), {})