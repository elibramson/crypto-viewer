from fastapi import Depends
from .http_client import CoinMarketClient
from .config import project_settings
from .interfaces.crypto_client import CryptoClientInterface

async def get_crypto_client() -> CryptoClientInterface:
    """
    Dependency provider for the crypto client.
    Creates a new client instance for each request and ensures proper cleanup.
    """
    client = CoinMarketClient(
        base_url="https://pro-api.coinmarketcap.com",
        api_key=project_settings.COIN_API_TOKEN
    )
    try:
        yield client
    finally:
        await client.session.close() 