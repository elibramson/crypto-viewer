from .config import project_settings
from .http_client import CoinMarketClient


#TODO: Move to dependency injection
coin_service = CoinMarketClient(
    base_url="https://pro-api.coinmarketcap.com",
    api_key=project_settings.COIN_API_TOKEN
)

