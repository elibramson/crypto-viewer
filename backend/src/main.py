from fastapi import FastAPI
from .config import project_settings
from .http_client import CoinMarketClient
from .router import router as coin_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(coin_router)

# Debug line to confirm API token is loaded
print("API Token loaded:", bool(project_settings.COIN_API_TOKEN))

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)