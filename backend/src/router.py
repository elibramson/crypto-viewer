from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict, Any
from .dependencies import get_crypto_client
from .interfaces.crypto_client import CryptoClientInterface
import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/cryptocurrencies",
    tags=["cryptocurrencies"]
)

@router.get("", response_model=List[Dict[str, Any]])
async def list_coins(
    crypto_client: CryptoClientInterface = Depends(get_crypto_client)
):
    try:
        return await crypto_client.get_listing()
    except Exception as e:
        logger.error(f"Error fetching cryptocurrency listings: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch cryptocurrency listings"
        )

@router.get("/{currency_id}", response_model=Dict[str, Any])
async def coin_details(
    currency_id: int,
    crypto_client: CryptoClientInterface = Depends(get_crypto_client)
):
    try:
        result = await crypto_client.get_currency_info(currency_id)
        if not result:
            raise HTTPException(
                status_code=404,
                detail=f"Cryptocurrency with ID {currency_id} not found"
            )
        return result
    except Exception as e:
        logger.error(f"Error fetching cryptocurrency details: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch cryptocurrency details"
        )