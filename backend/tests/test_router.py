import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.http_client import CoinMarketClient, CryptoAPIError

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

@pytest.fixture
def test_client():
    """Create a test client for the FastAPI application"""
    return TestClient(app)

@pytest.fixture
def mock_crypto_client(mocker):
    """Mock the crypto client for testing"""
    mock = mocker.patch.object(CoinMarketClient, 'get_listing')
    mock.return_value = MOCK_LISTING_RESPONSE["data"]
    return mock

@pytest.fixture
def mock_currency_info(mocker):
    """Mock the currency info method for testing"""
    mock = mocker.patch.object(CoinMarketClient, 'get_currency_info')
    mock.return_value = MOCK_CURRENCY_INFO_RESPONSE["data"]["1"]
    return mock

def test_list_coins_success(test_client, mock_crypto_client):
    """Test successful cryptocurrency listing endpoint"""
    response = test_client.get("/cryptocurrencies")
    assert response.status_code == 200
    assert response.json() == MOCK_LISTING_RESPONSE["data"]
    mock_crypto_client.assert_called_once()

def test_coin_details_success(test_client, mock_currency_info):
    """Test successful currency details endpoint"""
    response = test_client.get("/cryptocurrencies/1")
    assert response.status_code == 200
    assert response.json() == MOCK_CURRENCY_INFO_RESPONSE["data"]["1"]
    mock_currency_info.assert_called_once_with(1)

def test_list_coins_error(test_client, mock_crypto_client):
    """Test error handling in cryptocurrency listing endpoint"""
    mock_crypto_client.side_effect = CryptoAPIError("API Error")
    response = test_client.get("/cryptocurrencies")
    assert response.status_code == 500
    assert "Failed to fetch cryptocurrency listings" in response.json()["detail"]

def test_coin_details_error(test_client, mock_currency_info):
    """Test error handling in currency details endpoint"""
    mock_currency_info.side_effect = CryptoAPIError("API Error")
    response = test_client.get("/cryptocurrencies/1")
    assert response.status_code == 500
    assert "Failed to fetch cryptocurrency details" in response.json()["detail"] 