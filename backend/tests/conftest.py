import pytest
import aiohttp
from unittest.mock import AsyncMock, MagicMock
from src.http_client import CoinMarketClient, CryptoAPIError, APIRateLimitError, APIAuthenticationError

@pytest.fixture
def mock_response():
    """Fixture for creating mock responses"""
    def _create_mock_response(status=200, data=None):
        mock = AsyncMock()
        mock.status = status
        mock.json = AsyncMock(return_value=data or {})
        return mock
    return _create_mock_response

@pytest.fixture
def mock_session():
    """Fixture for creating a mock aiohttp session"""
    session = AsyncMock(spec=aiohttp.ClientSession)
    session.closed = False
    return session

@pytest.fixture
async def crypto_client(mock_session):
    """Fixture for creating a CoinMarketClient instance with a mock session"""
    client = CoinMarketClient(
        base_url="https://test-api.coinmarketcap.com",
        api_key="test-api-key"
    )
    client._session = mock_session
    yield client
    await client.close() 