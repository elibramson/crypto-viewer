from aiohttp import ClientSession
from async_lru import alru_cache
from typing import Dict, List, Any
from .interfaces.crypto_client import CryptoClientInterface
from functools import lru_cache
from .config import project_settings

class HttpClient:
    def __init__(self, base_url: str, api_key: str):
        self.session = ClientSession(
            base_url=base_url,
            headers={
                "X-CMC_PRO_API_KEY": api_key,
            },
        )

class CoinMarketClient(HttpClient, CryptoClientInterface):
    # Class-level cache for all instances
    _listing_cache = {}
    _currency_info_cache = {}

    @classmethod
    @alru_cache(maxsize=100)
    async def get_listing(cls) -> List[Dict[str, Any]]:
        # Create a temporary instance to make the request
        instance = cls(
            base_url="https://pro-api.coinmarketcap.com",
            api_key=project_settings.COIN_API_TOKEN
        )
        try:
            async with instance.session.get("/v1/cryptocurrency/listings/latest") as response:
                result = await response.json()
                if response.status != 200:
                    raise Exception(f"API Error: {result.get('status', {}).get('error_message', 'Unknown error')}")
                return result.get("data", [])
        finally:
            await instance.session.close()

    @classmethod
    @alru_cache(maxsize=100)
    async def get_currency_info(cls, currency_id: int) -> Dict[str, Any]:
        # Create a temporary instance to make the request
        instance = cls(
            base_url="https://pro-api.coinmarketcap.com",
            api_key=project_settings.COIN_API_TOKEN
        )
        try:
            async with instance.session.get(
                "/v2/cryptocurrency/quotes/latest",
                params={"id": currency_id}
            ) as response:
                result = await response.json()
                if response.status != 200:
                    raise Exception(f"API Error: {result.get('status', {}).get('error_message', 'Unknown error')}")
                return result.get("data", {}).get(str(currency_id), {})
        finally:
            await instance.session.close()