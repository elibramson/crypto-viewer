import pytest
from src.dependencies import get_crypto_client
from src.http_client import CoinMarketClient

@pytest.mark.asyncio
async def test_get_crypto_client():
    """Test the crypto client dependency"""
    async for client in get_crypto_client():
        # Assert
        assert isinstance(client, CoinMarketClient)
        assert client.base_url == "https://pro-api.coinmarketcap.com"
        assert client.api_key is not None

        # Get the session to ensure it exists
        session = await client.session
        assert session is not None

        # Test session cleanup
        await client.close()
        assert session.closed 