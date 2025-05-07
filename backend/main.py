from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from dotenv import load_dotenv
import requests
import os
import time

# Load local .env
load_dotenv()

# Config
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")
STOCK_SYMBOL = "AAPL"  # ✅ Set your symbol here once

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://ai-stock-predictorr.netlify.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": f"FastAPI + Finnhub backend for {STOCK_SYMBOL}"}


@app.get("/stock-history")
def stock_history():
    print(f"📡 Fetching {STOCK_SYMBOL} stock data from Finnhub...")

    if not FINNHUB_API_KEY:
        print("❌ Missing API key")
        return {"error": "Missing API key"}

    # Get timestamps for the past 30 days
    end = int(time.time())
    start = end - 60 * 60 * 24 * 30

    url = "https://finnhub.io/api/v1/stock/candle"
    params = {
        "symbol": STOCK_SYMBOL,
        "resolution": "D",
        "from": start,
        "to": end,
        "token": FINNHUB_API_KEY,
    }

    response = requests.get(url, params=params)
    data = response.json()

    print(f"🧾 Raw response for {STOCK_SYMBOL}:", data)

    if data.get("s") != "ok":
        print(f"❌ Finnhub error for {STOCK_SYMBOL}:", data)
        return []

    history = []
    for ts, close in zip(data["t"], data["c"]):
        date_str = datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
        history.append({"date": date_str, "close": round(close, 2)})

    print(f"✅ Fetched {len(history)} rows for {STOCK_SYMBOL}")
    return history