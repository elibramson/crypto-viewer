import pytest
import aiohttp
from src.http_client import (
    CoinMarketClient,
    CryptoAPIError,
    APIRateLimitError,
    APIAuthenticationError
)

# Test data
MOCK_LISTING_RESPONSE = {
    "data": [
        {
            "id": 1,
            "name": "Bitcoin",
            "symbol": "BTC",
            "quote": {"USD": {"price": 50000.0}}
        }
    ]
}

MOCK_CURRENCY_INFO_RESPONSE = {
    "data": {
        "1": {
            "id": 1,
            "name": "Bitcoin",
            "symbol": "BTC",
            "quote": {"USD": {"price": 50000.0}}
        }
    }
}

@pytest.mark.asyncio
async def test_get_listing_success(crypto_client, mock_response):
    """Test successful cryptocurrency listing retrieval"""
    # Arrange
    mock_resp = mock_response(status=200, data=MOCK_LISTING_RESPONSE)
    crypto_client._session.get.return_value.__aenter__.return_value = mock_resp

    # Act
    result = await crypto_client.get_listing()

    # Assert
    assert result == MOCK_LISTING_RESPONSE["data"]
    crypto_client._session.get.assert_called_once_with(
        "/v1/cryptocurrency/listings/latest",
        params=None
    )

@pytest.mark.asyncio
async def test_get_currency_info_success(crypto_client, mock_response):
    """Test successful currency info retrieval"""
    # Arrange
    mock_resp = mock_response(status=200, data=MOCK_CURRENCY_INFO_RESPONSE)
    crypto_client._session.get.return_value.__aenter__.return_value = mock_resp

    # Act
    result = await crypto_client.get_currency_info(1)

    # Assert
    assert result == MOCK_CURRENCY_INFO_RESPONSE["data"]["1"]
    crypto_client._session.get.assert_called_once_with(
        "/v2/cryptocurrency/quotes/latest",
        params={"id": 1}
    )

@pytest.mark.asyncio
async def test_get_listing_rate_limit(crypto_client, mock_response):
    """Test rate limit error handling"""
    # Arrange
    mock_resp = mock_response(
        status=429,
        data={"status": {"error_message": "Rate limit exceeded"}}
    )
    crypto_client._session.get.return_value.__aenter__.return_value = mock_resp

    # Act & Assert
    with pytest.raises(APIRateLimitError):
        await crypto_client.get_listing()

@pytest.mark.asyncio
async def test_get_listing_auth_error(crypto_client, mock_response):
    """Test authentication error handling"""
    # Arrange
    mock_resp = mock_response(
        status=401,
        data={"status": {"error_message": "Invalid API key"}}
    )
    crypto_client._session.get.return_value.__aenter__.return_value = mock_resp

    # Act & Assert
    with pytest.raises(APIAuthenticationError):
        await crypto_client.get_listing()

@pytest.mark.asyncio
async def test_get_listing_generic_error(crypto_client, mock_response):
    """Test generic error handling"""
    # Arrange
    mock_resp = mock_response(
        status=500,
        data={"status": {"error_message": "Internal server error"}}
    )
    crypto_client._session.get.return_value.__aenter__.return_value = mock_resp

    # Act & Assert
    with pytest.raises(CryptoAPIError):
        await crypto_client.get_listing()

@pytest.mark.asyncio
async def test_session_lazy_initialization():
    """Test lazy session initialization"""
    # Arrange
    client = CoinMarketClient(
        base_url="https://test-api.coinmarketcap.com",
        api_key="test-api-key"
    )

    # Assert
    assert client._session is None

    # Act
    session = await client.session

    # Assert
    assert session is not None
    assert isinstance(session, aiohttp.ClientSession)

    # Cleanup
    await client.close()

@pytest.mark.asyncio
async def test_session_cleanup():
    """Test session cleanup"""
    # Arrange
    client = CoinMarketClient(
        base_url="https://test-api.coinmarketcap.com",
        api_key="test-api-key"
    )
    session = await client.session

    # Act
    await client.close()

    # Assert
    assert session.closed 