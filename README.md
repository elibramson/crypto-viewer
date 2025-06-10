# Crypto Viewer Educational Project

This repository is an **educational project** designed to validate and demonstrate a full stack application using **React** (frontend) and **FastAPI** (backend).

## Project Overview

- **Backend:** FastAPI (Python)
- **Frontend:** React (JavaScript/TypeScript)
- **Purpose:** Educational, for learning and validating full stack development patterns and API integration.

## Features

- Cryptocurrency data retrieval from CoinMarketCap API (backend)
- Example API endpoints for listing and querying cryptocurrencies
- Ready for integration with a React frontend
- Comprehensive test suite with high coverage
- Dependency injection for better maintainability
- Efficient HTTP client with caching and error handling

## Getting Started

### Backend

1. **Install dependencies:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

2. **Set up environment variables:**
    - Create a `.env` file in the project root with your CoinMarketCap API key:
      ```
      COIN_API_TOKEN=your_coinmarketcap_api_key
      ```

3. **Run the FastAPI server:**
    ```bash
    uvicorn backend.src.main:app --reload
    ```

4. **API Docs:**  
   Visit [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for interactive API documentation.

### Testing

1. **Install test dependencies:**
    ```bash
    pip install -e ".[test]"
    ```

2. **Run tests:**
    ```bash
    cd backend
    pytest
    ```

3. **Run tests with coverage:**
    ```bash
    pytest --cov=src
    ```

The test suite includes:
- Unit tests for HTTP client
- Integration tests for API endpoints
- Error handling tests
- Session management tests
- Dependency injection tests

### Project Structure

```
backend/
├── src/
│   ├── interfaces/      # Interface definitions
│   ├── http_client.py   # HTTP client implementation
│   ├── router.py        # API endpoints
│   ├── dependencies.py  # Dependency injection
│   ├── config.py        # Configuration
│   └── main.py         # Application entry point
├── tests/
│   ├── test_http_client.py
│   ├── test_router.py
│   └── test_dependencies.py
└── pytest.ini          # Test configuration
```

### Frontend

- In progress

## Disclaimer

This project is for educational purposes only.  
It is not intended for production use.
