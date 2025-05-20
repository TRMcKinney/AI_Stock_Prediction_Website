import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3" #suppress TensorFlow warnings in the logs

import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client, Client
from dotenv import load_dotenv
from datetime import datetime
import requests
import time
import subprocess
import pandas as pd
from model import train_and_predict

# Load environment variables from .env
load_dotenv()

# Constants
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Fail early if any critical variable is missing
if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("Supabase credentials are missing from environment variables.")

if not ALPHA_VANTAGE_API_KEY:
    raise RuntimeError("Alpha Vantage API key is missing from environment variables.")

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
    response = supabase.table("stock_prices").select("*").order("timestamp").execute()
    df = pd.DataFrame(response.data)
    if df.empty:
        return {"error": "No data available"}
    
    try:
        result = train_and_predict(df)
        return result
    except ValueError as e:
        return {"error": str(e)}

#@app.get("/row-count")
#def row_count():
#    print("Counting rows in Supabase...")
#    response = supabase.table("stock_prices").select("id", count="exact").execute()
#    return {"count": response.count or 0}

@app.get("/")
def root():
    return {"message": f"FastAPI + Alpha Vantage backend for {STOCK_SYMBOL}"}


@app.get("/stock-100") # gets latest 100 stock rows for stock chart
def stock_100():
    print("Fetching latest 100 stock rows from Supabase for chart...")

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

@app.get("/stock-stats")
def stock_stats():
    print("Fetching stock stats (count and date range)...")
    
    # Get full row count
    count_res = supabase.table("stock_prices").select("id", count="exact").execute()
    row_count = count_res.count or 0

    # Get earliest and latest timestamps (note: using timestamp not date)
    min_date_res = supabase.table("stock_prices").select("timestamp").order("timestamp", desc=False).limit(1).execute()
    max_date_res = supabase.table("stock_prices").select("timestamp").order("timestamp", desc=True).limit(1).execute()

    min_date = min_date_res.data[0]["timestamp"] if min_date_res.data else None
    max_date = max_date_res.data[0]["timestamp"] if max_date_res.data else None

    return {
        "count": row_count,
        "min_date": min_date,
        "max_date": max_date
    }



@app.post("/fetch-latest")
def fetch_latest():
    try:
        print("Triggering data fetch...")
        python_executable = sys.executable  # path to current Python (inside venv)
        result = subprocess.run(
            [python_executable, "fetch_and_upload.py"],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(__file__)  # ensure working dir is backend/
        )
        if result.returncode == 0:
            return {"status": "success", "output": result.stdout}
        else:
            return {"status": "error", "output": result.stderr}

    except Exception as e:
        return {"status": "error", "message": str(e)}