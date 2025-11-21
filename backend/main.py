import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

import sys
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client
from dotenv import load_dotenv
from datetime import datetime, timedelta
from threading import Lock
import subprocess
import pandas as pd
import baseline_model
import cross_validation_model
import persist_model
import grid_search_model
from fastapi.responses import StreamingResponse
import json
from prediction_history import insert_predictions, refresh_missing_actuals

# Load env vars
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
# ALPHA_VANTAGE_API_KEY is no longer strictly needed for the fetch, 
# but we keep it if other parts use it or for safety.

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("Supabase credentials are missing.")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

STOCK_SYMBOL = "AAPL"

app = FastAPI()

# --- Caching Logic (Unchanged) ---
CACHE_TTL_SECONDS = int(os.getenv("STOCK_CACHE_TTL_SECONDS", "300"))
_stock_cache_lock = Lock()
_stock_cache = {"df": None, "expires": datetime.min}

def _fetch_stock_prices_from_supabase():
    page_size = 1000
    start = 0
    frames = []
    while True:
        end = start + page_size - 1
        response = (
            supabase.table("stock_prices")
            .select("*")
            .order("timestamp")
            .range(start, end)
            .execute()
        )
        rows = response.data or []
        if not rows:
            break
        frames.append(pd.DataFrame(rows))
        if len(rows) < page_size:
            break
        start += page_size

    if not frames:
        raise ValueError("No data available")
    return pd.concat(frames, ignore_index=True)

def get_stock_dataframe(force_refresh: bool = False) -> pd.DataFrame:
    now = datetime.utcnow()
    if not force_refresh:
        with _stock_cache_lock:
            if _stock_cache["df"] is not None and now < _stock_cache["expires"]:
                return _stock_cache["df"].copy()

    df = _fetch_stock_prices_from_supabase()

    with _stock_cache_lock:
        _stock_cache["df"] = df
        _stock_cache["expires"] = now + timedelta(seconds=CACHE_TTL_SECONDS)

    return df.copy()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://ai-stock-predictorr.netlify.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": f"FastAPI + yfinance backend for {STOCK_SYMBOL}"}

@app.get("/predict")
def predict(models: str = Query("")):
    try:
        df = get_stock_dataframe()
    except ValueError as exc:
        return {"error": str(exc)}
    available = {
        "baseline": baseline_model.train_and_predict,
        "cross_validation": cross_validation_model.train_and_predict,
        "persist": persist_model.train_and_predict,
        "grid_search": grid_search_model.train_and_predict,
    }
    selected = models.split(",") if models else available.keys()
    try:
        results = {name: available[name](df) for name in selected if name in available}
        insert_predictions(results, df["close"].iloc[-1])
        return results
    except ValueError as e:
        return {"error": str(e)}

@app.get("/predict-stream")
def predict_stream(models: str = Query("")):
    def stream():
        try:
            df = get_stock_dataframe()
        except ValueError:
            yield "ERROR:No data available\n"
            return
        available = {
            "baseline": baseline_model.train_and_predict,
            "cross_validation": cross_validation_model.train_and_predict,
            "persist": persist_model.train_and_predict,
            "grid_search": grid_search_model.train_and_predict,
        }
        selected = models.split(",") if models else available.keys()
        model_list = [(name, available[name]) for name in selected if name in available]
        results = {}
        for name, fn in model_list:
            yield f"START:{name}\n"
            try:
                results[name] = fn(df)
            except ValueError as e:
                yield f"ERROR:{str(e)}\n"
                return
            yield f"END:{name}\n"
        insert_predictions(results, df["close"].iloc[-1])
        yield "RESULTS:" + json.dumps(results) + "\n"

    return StreamingResponse(stream(), media_type="text/plain")

@app.get("/prediction-history")
def prediction_history():
    resp = (
        supabase.table("prediction_histories")
        .select("*")
        .order("date_of_prediction", desc=True)
        .execute()
    )
    return resp.data or []

@app.post("/refresh-prediction-history")
def refresh_prediction_history():
    updated = refresh_missing_actuals()
    return {"updated": updated}

@app.get("/stock-100")
def stock_100():
    try:
        df = get_stock_dataframe()
    except ValueError:
        return []
    latest = df.tail(100).copy()
    latest.sort_values("timestamp", inplace=True)
    return [
        {"date": row["timestamp"], "close": round(row["close"], 2)}
        for row in latest.to_dict(orient="records")
    ]

@app.get("/stock-stats")
def stock_stats():
    try:
        df = get_stock_dataframe()
    except ValueError:
        return {"count": 0, "min_date": None, "max_date": None}

    return {
        "count": int(df.shape[0]),
        "min_date": df["timestamp"].iloc[0] if not df.empty else None,
        "max_date": df["timestamp"].iloc[-1] if not df.empty else None,
    }

# === UPDATED FETCH ENDPOINT ===
@app.post("/fetch-latest-stream")
def fetch_latest_stream():
    def stream_logs():
        # We removed the rate limit check because yfinance allows frequent access
        yield "Connecting to Yahoo Finance via yfinance...\n"

        process = subprocess.Popen(
            [sys.executable, "fetch_and_upload.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )

        for line in process.stdout:
            yield line

        process.wait()
        
        # Refresh cache immediately
        try:
            get_stock_dataframe(force_refresh=True)
        except ValueError:
            pass
            
        yield f"\nDone. Exit code: {process.returncode}\n"

    return StreamingResponse(stream_logs(), media_type="text/plain")

@app.get("/ping")
def ping():
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}
