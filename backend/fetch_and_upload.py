# code to fetch the apple stock data from the API and upload it to the database (supabase)

import os
import requests
from datetime import datetime
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv() # This reads from .env locally

# === CONFIG ===
ALPHA_VANTAGE_API_KEY = os.environ["ALPHA_VANTAGE_API_KEY"]
SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_KEY"]

TABLE_NAME = "stock_prices"
SYMBOL = "AAPL"

# === SUPABASE CLIENT ===
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# === ALPHA VANTAGE CALL ===
def get_daily_stock_data(symbol: str):
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_DAILY",  # free-tier supported
        "symbol": symbol,
        "outputsize": "compact",          # up to ~100 recent days
        "apikey": ALPHA_VANTAGE_API_KEY
    }

    print(f"Requesting Alpha Vantage with: {url} | params={params}")
    
    r = requests.get(url, params=params)
    data = r.json()

    if "Time Series (Daily)" not in data:
        print("Failed to fetch stock data:", data)
        return []

    time_series = data["Time Series (Daily)"]
    records = []

    for date_str, values in time_series.items():
        records.append({
            "timestamp": date_str,
            "open": float(values["1. open"]),
            "high": float(values["2. high"]),
            "low": float(values["3. low"]),
            "close": float(values["4. close"]),
            "volume": float(values["5. volume"])
        })

    print(f"Retrieved {len(records)} records.")
    return records

# === UPSERT TO SUPABASE ===
def upload_to_supabase(records):
    print("Uploading to Supabase...")
    inserted_count = 0
    for row in records:
        existing = supabase.table(TABLE_NAME).select("id").eq("timestamp", row["timestamp"]).execute()

        if len(existing.data) == 0:
            supabase.table(TABLE_NAME).insert(row).execute()
            inserted_count += 1
            print(f"   Inserted: {row['timestamp']}")
        else:
            print(f"   Skipped duplicate: {row['timestamp']}")

    print("Upload complete.")
    return inserted_count


def fetch_and_upload():
    data = get_daily_stock_data(SYMBOL)
    print(f"Fetched {len(data)} records from Alpha Vantage.")
    if data:
        inserted_count = upload_to_supabase(data)
        print(f"Success: Uploaded {inserted_count} new records to Supabase.")
        return inserted_count
    else:
        print("No data fetched from Alpha Vantage.")
        return 0

if __name__ == "__main__":
    fetch_and_upload()