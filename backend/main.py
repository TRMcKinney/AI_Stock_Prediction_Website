from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from datetime import datetime
import os
import requests
import time

# Load environment variables from .env
load_dotenv()

# Constants
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
STOCK_SYMBOL = "AAPL"

app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Local Vue dev server
        "https://ai-stock-predictorr.netlify.app"  # Deployed frontend
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": f"FastAPI + Alpha Vantage backend for {STOCK_SYMBOL}"}


@app.get("/stock-history")
def stock_history():
    print(f"📡 Fetching {STOCK_SYMBOL} stock data from Alpha Vantage...")

    if not ALPHA_VANTAGE_API_KEY:
        print("❌ API key missing")
        return {"error": "Missing API key"}

    url = "https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_DAILY",  # FREE endpoint
        "symbol": STOCK_SYMBOL,
        "outputsize": "compact",  # ~last 100 days
        "apikey": ALPHA_VANTAGE_API_KEY,
    }

    # Optional: be kind to their rate limit
    time.sleep(1)

    response = requests.get(url, params=params)
    data = response.json()

    # Handle errors and rate limit messages
    if "Time Series (Daily)" not in data:
        print("❌ Error:", data.get("Note") or data.get("Error Message") or data)
        return []

    series = data["Time Series (Daily)"]

    # Format for chart (date ascending)
    history = []
    for date_str, values in sorted(series.items()):
        close = float(values["4. close"])
        history.append({"date": date_str, "close": round(close, 2)})

    print(f"✅ Fetched {len(history)} rows for {STOCK_SYMBOL}")
    return history
