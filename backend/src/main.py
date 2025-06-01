from fastapi import FastAPI
from .config import project_settings
from .http_client import CoinMarketClient
from .router import router as coin_router

app = FastAPI()

app.include_router(coin_router)

# Debug line to confirm API token is loaded
print("API Token loaded:", bool(project_settings.COIN_API_TOKEN))

