from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from .config import project_settings
from .http_client import CoinMarketClient, CryptoAPIError
from .router import router as coin_router
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Crypto API",
    description="API for cryptocurrency data",
    version="1.0.0"
)

# CORS configuration - Update this to match your frontend URL
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",  # Add any other frontend URLs you need
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Error handling middleware
@app.exception_handler(CryptoAPIError)
async def crypto_api_exception_handler(request: Request, exc: CryptoAPIError):
    logger.error(f"Crypto API error: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"message": str(exc)}
    )

# Initialize HTTP client
http_client = CoinMarketClient(
    base_url="https://pro-api.coinmarketcap.com",
    api_key=project_settings.COIN_API_TOKEN
)

# Include router
app.include_router(coin_router)

@app.on_event("startup")
async def startup_event():
    logger.info("Starting up the application...")
    logger.info(f"API Token loaded: {bool(project_settings.COIN_API_TOKEN)}")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down the application...")
    await http_client.close()