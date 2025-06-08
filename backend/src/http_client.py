from aiohttp import ClientSession
from async_lru import alru_cache
from typing import Dict, List, Any, Optional
from .interfaces.crypto_client import CryptoClientInterface
from functools import lru_cache
from .config import project_settings
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class CryptoAPIError(Exception):
    """Base exception for crypto API errors"""
    pass

class APIRateLimitError(CryptoAPIError):
    """Exception for rate limit errors"""
    pass

class APIAuthenticationError(CryptoAPIError):
    """Exception for authentication errors"""
    pass

class HttpClient:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.api_key = api_key
        self._session: Optional[ClientSession] = None

    @property
    async def session(self) -> ClientSession:
        """Lazy initialization of the session"""
        if self._session is None or self._session.closed:
            self._session = ClientSession(
                base_url=self.base_url,
                headers={
                    "X-CMC_PRO_API_KEY": self.api_key,
                },
            )
        return self._session

    async def close(self):
        """Close the session"""
        if self._session and not self._session.closed:
            await self._session.close()

class CoinMarketClient(HttpClient, CryptoClientInterface):
    # Cache configuration
    CACHE_TTL = timedelta(minutes=5)
    MAX_CACHE_SIZE = 100

    def __init__(self, base_url: str, api_key: str):
        super().__init__(base_url, api_key)
        self._cache = {}
        self._cache_timestamps = {}

    def _is_cache_valid(self, key: str) -> bool:
        """Check if the cache entry is still valid"""
        if key not in self._cache_timestamps:
            return False
        return datetime.now() - self._cache_timestamps[key] < self.CACHE_TTL

    async def _make_request(self, endpoint: str, params: Dict = None) -> Dict:
        """Make an HTTP request with proper error handling"""
        try:
            session = await self.session
            async with session.get(endpoint, params=params) as response:
                result = await response.json()
                
                if response.status == 429:
                    raise APIRateLimitError("Rate limit exceeded")
                elif response.status == 401:
                    raise APIAuthenticationError("Invalid API key")
                elif response.status != 200:
                    raise CryptoAPIError(
                        f"API Error: {result.get('status', {}).get('error_message', 'Unknown error')}"
                    )
                
                return result
        except Exception as e:
            logger.error(f"Error making request to {endpoint}: {str(e)}")
            raise

    @alru_cache(maxsize=MAX_CACHE_SIZE)
    async def get_listing(self) -> List[Dict[str, Any]]:
        """
        Get the latest cryptocurrency listings.
        
        Returns:
            List[Dict[str, Any]]: List of cryptocurrency data
            
        Raises:
            CryptoAPIError: If the API request fails
        """
        result = await self._make_request("/v1/cryptocurrency/listings/latest")
        return result.get("data", [])

    @alru_cache(maxsize=MAX_CACHE_SIZE)
    async def get_currency_info(self, currency_id: int) -> Dict[str, Any]:
        """
        Get detailed information about a specific cryptocurrency.
        
        Args:
            currency_id (int): The ID of the cryptocurrency
            
        Returns:
            Dict[str, Any]: Detailed cryptocurrency information
            
        Raises:
            CryptoAPIError: If the API request fails
        """
        result = await self._make_request(
            "/v2/cryptocurrency/quotes/latest",
            params={"id": currency_id}
        )
        return result.get("data", {}).get(str(currency_id), {})