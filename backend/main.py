from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import yfinance as yf
import pandas as pd

app = FastAPI()

# Allow requests from your Vue frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "FastAPI backend is running"}

@app.get("/stock-history")
def stock_history():
    import yfinance as yf
    import pandas as pd

    df = yf.download("AAPL", period="1mo", interval="1d", group_by="ticker")

    if df.empty:
        return []

    df.reset_index(inplace=True)

    # Flatten multi-index columns
    df.columns = ['_'.join(col).strip() if isinstance(col, tuple) else col for col in df.columns]
    # Print flattened column names
    print("📊 Flattened columns:", df.columns)

    # Check what the 'date' column is actually called
    date_col = [col for col in df.columns if col.lower().startswith("date")][0]
    close_col = [col for col in df.columns if "close" in col.lower() and "aapl" in col.lower()][0]

    print("📆 Date column:", date_col)
    print("💰 Close column:", close_col)

    history = [
        {
            "date": row[date_col].strftime("%Y-%m-%d"),
            "close": round(row[close_col], 2)
        }
        for _, row in df.iterrows()
    ]

    return history