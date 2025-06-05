from fastapi import APIRouter, Depends
from .dependencies import get_crypto_client
from .interfaces.crypto_client import CryptoClientInterface
from .http_client import CoinMarketClient

router = APIRouter(
    prefix="/cryptocurrencies"
)

@router.get("")
async def list_coins():
    return await CoinMarketClient.get_listing()

@router.get("/{currency_id}")
async def coin_details(currency_id: int):
    return await CoinMarketClient.get_currency_info(currency_id)