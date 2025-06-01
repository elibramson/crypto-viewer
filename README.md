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

### Frontend

- In progress

## Disclaimer

This project is for educational purposes only.  
It is not intended for production use.
