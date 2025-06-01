from fastapi import APIRouter
from .init import coin_service

router = APIRouter(
    prefix="/cryptocurrencies"
)

@router.get("")
async def list_coins():
    return await coin_service.get_listing()

@router.get("/{currency_id}")
async def coin_details(currency_id: int):
    return await coin_service.get_currency_info(currency_id)