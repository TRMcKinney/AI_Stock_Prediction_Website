import os
import requests
from datetime import datetime
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

# Config
ALPHA_VANTAGE_API_KEY = os.environ["ALPHA_VANTAGE_API_KEY"]
SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_KEY"]
TABLE_NAME = "stock_prices"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
SYMBOL = "AAPL"

def get_daily_stock_data(symbol):
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "outputsize": "compact",
        "apikey": ALPHA_VANTAGE_API_KEY
    }

    r = requests.get(url, params=params)
    data = r.json()

    if "Time Series (Daily)" not in data:
        print("Failed to fetch stock data:", data)
        return []

    return [
        {
            "timestamp": date_str,
            "open": float(values["1. open"]),
            "high": float(values["2. high"]),
            "low": float(values["3. low"]),
            "close": float(values["4. close"]),
            "volume": float(values["5. volume"]),
        }
        for date_str, values in data["Time Series (Daily)"].items()
    ]

def upload_to_supabase(records):
    print("Uploading to Supabase...")
    inserted_count = 0
    for row in records:
        exists = supabase.table(TABLE_NAME).select("id").eq("timestamp", row["timestamp"]).execute()
        if not exists.data:
            supabase.table(TABLE_NAME).insert(row).execute()
            inserted_count += 1
            print(f"   Inserted: {row['timestamp']}")
        else:
            print(f"   Skipped duplicate: {row['timestamp']}")
    return inserted_count

def fetch_and_upload():
    today = datetime.today().strftime('%Y-%m-%d')
    count_res = supabase.table("fetch_metadata").select("value").eq("date", today).maybe_single().execute()
    fetch_count = int(count_res.data["value"]) if count_res and count_res.data else 0

    if fetch_count >= 25:
        print("API rate limit reached, skipping.")
        return 0

    data = get_daily_stock_data(SYMBOL)
    if not data:
        print("No data fetched.")
        return 0

    uploaded = upload_to_supabase(data)

    # Update or insert today's fetch count
    new_count = fetch_count + 1

    # SAFELY handle first-time use when no row exists yet
    if count_res and count_res.data:
        print(f"Updating fetch count to {new_count} for {today}")
        supabase.table("fetch_metadata").update({"value": str(new_count)}).eq("date", today).execute()
    else:
        print(f"First fetch today — inserting row with count {new_count} for {today}")
        supabase.table("fetch_metadata").insert({"date": today, "value": str(new_count)}).execute()
        
    return uploaded

if __name__ == "__main__":
    fetch_and_upload()
