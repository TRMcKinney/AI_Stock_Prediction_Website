from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from dotenv import load_dotenv
import requests
import os
import time

# Load .env (for local development)
load_dotenv()

# Get API key (works both locally and on Render)
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")

app = FastAPI()

# CORS settings: allow local + deployed frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vue dev server
        "https://ai-stock-predictorr.netlify.app",  # Your Netlify site
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "Hello from FastAPI + Finnhub 👋"}


@app.get("/stock-history")
def stock_history():
    print("📡 Fetching AAPL stock data from Finnhub...")

    if not FINNHUB_API_KEY:
        print("❌ Missing API key")
        return {"error": "Missing API key"}

    # Get timestamps for the past 30 days
    end = int(time.time())
    start = end - 60 * 60 * 24 * 30

    url = "https://finnhub.io/api/v1/stock/candle"
    params = {
        "symbol": "AAPL",
        "resolution": "D",
        "from": start,
        "to": end,
        "token": FINNHUB_API_KEY,
    }

    response = requests.get(url, params=params)
    data = response.json()

    if data.get("s") != "ok":
        print("❌ Failed to fetch data:", data)
        return []

    history = []
    for ts, close in zip(data["t"], data["c"]):
        date_str = datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
        history.append({"date": date_str, "close": round(close, 2)})

    print(f"✅ Fetched {len(history)} rows")
    return history