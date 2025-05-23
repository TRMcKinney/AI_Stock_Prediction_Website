import os
import requests
from datetime import datetime
from supabase import create_client, Client
from dotenv import load_dotenv
import time

# === Load secrets ===
load_dotenv()

ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

TABLE_NAME = "stock_prices"
SYMBOL = "AAPL"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_full_history(symbol: str):
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "outputsize": "full",  # 👈 key difference here
        "apikey": ALPHA_VANTAGE_API_KEY
    }

    print(f"Fetching full history for {symbol}...")
    r = requests.get(url, params=params)
    data = r.json()

    if "Time Series (Daily)" not in data:
        print("❌ Failed to fetch stock data:", data)
        return []

    records = []
    for date_str, values in data["Time Series (Daily)"].items():
        records.append({
            "timestamp": date_str,
            "open": float(values["1. open"]),
            "high": float(values["2. high"]),
            "low": float(values["3. low"]),
            "close": float(values["4. close"]),
            "volume": float(values["5. volume"])
        })

    print(f"✅ Retrieved {len(records)} total rows.")
    return records

def upload_deduplicated(records):
    print("Checking existing timestamps...")
    existing_res = supabase.table(TABLE_NAME).select("timestamp").execute()
    existing_dates = set(row["timestamp"] for row in existing_res.data)

    to_upload = [r for r in records if r["timestamp"] not in existing_dates]

    print(f"📦 Uploading {len(to_upload)} new rows...")

    for row in to_upload:
        supabase.table(TABLE_NAME).insert(row).execute()
        print(f"   + {row['timestamp']}")
        time.sleep(0.1)  # Small delay to avoid rate limits

    print("✅ Upload complete.")

if __name__ == "__main__":
    data = get_full_history(SYMBOL)
    if data:
        upload_deduplicated(data)
