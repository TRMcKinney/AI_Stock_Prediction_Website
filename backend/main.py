from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client, Client
from dotenv import load_dotenv
from datetime import datetime
import os
import requests
import time
import subprocess
from model import train_and_predict

# Load environment variables from .env
load_dotenv()

# Constants
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# 🛑 Fail early if any critical variable is missing
if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("❌ Supabase credentials are missing from environment variables.")

if not ALPHA_VANTAGE_API_KEY:
    raise RuntimeError("❌ Alpha Vantage API key is missing from environment variables.")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

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

@app.get("/predict")
def predict():
    response = supabase.table("stock_prices").select("*").order("date").execute()
    df = pd.DataFrame(response.data)
    if df.empty:
        return {"error": "No data available"}
    
    result = train_and_predict(df)
    return result

@app.get("/row-count")
def row_count():
    print("📊 Counting rows in Supabase...")
    response = supabase.table("stock_prices").select("id", count="exact").execute()
    return {"count": response.count or 0}

@app.get("/")
def root():
    return {"message": f"FastAPI + Alpha Vantage backend for {STOCK_SYMBOL}"}


@app.get("/stock-history")
def stock_history():
    print("📡 Fetching latest 100 stock rows from Supabase...")

    response = supabase.table("stock_prices") \
        .select("*") \
        .order("timestamp", desc=True) \
        .limit(100) \
        .execute()

    data = response.data or []
    if not data:
        return []

    # sort by timestamp ascending (oldest to newest)
    sorted_data = sorted(data, key=lambda x: x["timestamp"])

    result = [
        {
            "date": row["timestamp"],
            "close": round(row["close"], 2)
        }
        for row in sorted_data
    ]
    return result

@app.post("/fetch-latest")
def fetch_latest():
    try:
        print("🚀 Triggering data fetch...")
        result = subprocess.run(["python", "fetch_and_upload.py"], capture_output=True, text=True)

        if result.returncode == 0:
            return {"status": "success", "output": result.stdout}
        else:
            return {"status": "error", "output": result.stderr}

    except Exception as e:
        return {"status": "error", "message": str(e)}