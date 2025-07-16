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

def _mask_key(text: str) -> str:
    """Mask occurrences of the API key in the provided text."""
    return text.replace(ALPHA_VANTAGE_API_KEY, "[REDACTED]")


def test_alpha_vantage() -> bool:
    """Attempt a small request to Alpha Vantage and return success status."""
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "GLOBAL_QUOTE",
        "symbol": "IBM",
        "apikey": ALPHA_VANTAGE_API_KEY,
    }
    try:
        r = requests.get(url, params=params, timeout=10)
        data = r.json()
    except Exception as e:
        print("Test request failed:", e)
        return False

    return "Global Quote" in data

def get_daily_stock_data(symbol):
    print("API key acquired.")
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "outputsize": "compact",
        "apikey": ALPHA_VANTAGE_API_KEY,
    }

    print("Connecting to Alpha Vantage...")
    try:
        r = requests.get(url, params=params, timeout=10)
        print("Retrieving data...")
        data = r.json()
    except Exception as e:
        print("Failed request:", e)
        return []

    if "Time Series (Daily)" not in data:
        sanitized = {k: _mask_key(str(v)) for k, v in data.items()}
        print("Failed to fetch stock data:", sanitized)
        return []

    records = [
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

    print(f"Retrieved {len(records)} records.")
    return records

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
    print(f"Fetch count for {today}: {fetch_count}")

    if fetch_count >= 25:
        print("API rate limit reached, skipping.")
        return 0

    print("Testing Alpha Vantage connection...")
    if test_alpha_vantage():
        print("Successfully retrieved test data from Alpha Vantage.")
    else:
        print("Failed to retrieve test data from Alpha Vantage.")

    print("Proceeding with fetch...")
    data = get_daily_stock_data(SYMBOL)
    if not data:
        print("No data fetched.")
        new_count = fetch_count + 1
        if count_res and count_res.data:
            print(f"Updating fetch count to {new_count} for {today}")
            supabase.table("fetch_metadata").update({"value": str(new_count)}).eq("date", today).execute()
        else:
            print(f"First fetch today — inserting row with count {new_count} for {today}")
            supabase.table("fetch_metadata").insert({"date": today, "value": str(new_count)}).execute()
        return 0

    uploaded = upload_to_supabase(data)
    print(f"Uploaded {uploaded} new rows.")

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
