import os
import yfinance as yf
from datetime import datetime
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

# Load Supabase credentials
SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_KEY"]
TABLE_NAME = "stock_prices"
SYMBOL = "AAPL"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def fetch_and_upload():
    print(f"Fetching data for {SYMBOL} via yfinance...")
    
    # Fetch data for the last month to ensure we catch recent days
    # yfinance handles the "API" part automatically without a key
    try:
        ticker = yf.Ticker(SYMBOL)
        hist = ticker.history(period="1y") 
    except Exception as e:
        print(f"Error fetching data from Yahoo: {e}")
        return 0
    
    if hist.empty:
        print("No data fetched.")
        return 0

    records = []
    # yfinance returns a DataFrame where the index is the Date
    for date, row in hist.iterrows():
        records.append({
            "timestamp": date.strftime('%Y-%m-%d'),
            "open": float(row["Open"]),
            "high": float(row["High"]),
            "low": float(row["Low"]),
            "close": float(row["Close"]),
            "volume": float(row["Volume"]),
        })

    print(f"Retrieved {len(records)} records. Uploading unique rows to Supabase...")
    
    inserted_count = 0
    for row in records:
        # Check if this timestamp already exists to avoid duplicates
        exists = supabase.table(TABLE_NAME).select("id").eq("timestamp", row["timestamp"]).execute()
        
        if not exists.data:
            supabase.table(TABLE_NAME).insert(row).execute()
            inserted_count += 1
            print(f"   Inserted: {row['timestamp']}")
        else:
            # Optional: Un-comment if you want to see skipped dates
            # print(f"   Skipped duplicate: {row['timestamp']}")
            pass
    
    print(f"Uploaded {inserted_count} new rows.")
    
    # We no longer need to track 'fetch_count' for rate limits, 
    # but we can log that we finished successfully.
    return inserted_count

if __name__ == "__main__":
    fetch_and_upload()
