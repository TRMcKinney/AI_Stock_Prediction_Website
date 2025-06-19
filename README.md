# AI Stock Prediction Website

This project demonstrates a simple stock prediction web application. The frontend is built with **Vue 3** and served by Vite, while the backend uses **FastAPI** and persists data to **Supabase** (PostgreSQL). The production site is hosted at <https://ai-stock-predictorr.netlify.app/>.

## Repository layout

- **frontend/** – Vue single page application
- **backend/** – FastAPI service and model code
- **tests/** – pytest suite for core functionality

## Backend overview

`backend/main.py` exposes several endpoints:

- **/predict** – train the model defined in `model.py` and return the latest prediction with a plot image.
- **/stock-100** – serve the most recent 100 rows for charting.
- **/stock-stats**, **/fetch-count**, **/last-fetch-date** – stats and API usage information.
- **/fetch-latest-stream** – run `fetch_and_upload.py` in a subprocess and stream logs.
- **/ping** – health check.

`fetch_and_upload.py` downloads prices from Alpha Vantage and saves new rows to Supabase, enforcing a 25‑request daily limit. `bulk_load_full_history.py` can populate the database with historical prices.

## Frontend overview

The Vue app displays prediction results and recent stock data. Key components include:

- **PredictionDetails.vue** – fetches results from `/predict`.
- **StockChart.vue** – renders closing prices returned by `/stock-100`.
- **FetchButton.vue** and **FetchLogsModal.vue** – trigger data fetches and show streaming logs from the backend.

## Running locally

1. **Start the backend**

   ```bash
   cd backend
   # activate a virtual environment and install requirements once
   uvicorn main:app --reload
   ```
   (See `backend/README.txt` for a quick reference.)

2. **Run the frontend**

   ```bash
   cd frontend
   npm install   # first time only
   npm run dev
   ```
   (See `frontend/README.txt` for details.)

## Running tests

Install the backend dependencies and run `pytest` from the repository root:

```bash
pip install -r backend/requirements.txt
pytest
```

The model training routine expects at least 210 rows of stock price data so that moving averages and 10‑day look‑backs can be computed.

## To Do

- Make data checker into a button for manual checking – the automatic function when fetching new data doesn't seem to work
- Have a model selector dropdown to select version of the predicting model
  - basic feed-forward neural network (the current one) – although needs fine tuning still
  - LSTM with memory
  - LSTM with memory and sentiment analysis module
- Then will need new database table to track predictions and by which model
- Table/visualisation for each model's past results and their accuracy
- New card with generic stock data analysis – (Balance Sheet values, total Revenue, Net Income, Operating Costs, Costs of Revenue, Operating Income, (Operating Income / Total Revenue) x 100, Earnings Per Share (EPS), Price-to-Earnings Ratio (P/E), Price to Sales Ratio (P/S), Debt to Equity Ratio, Return on Equity (ROE), Trend Analysis, Support and Resistance Levels, Moving Averages, Relative Strength Index (RSI), Valuation Metrics, Discounted Cash Fow (DCF) Analysis, Enterprise Value (EV/EBITDA), PEG Ratio)
  Another model version (LSTM with memory and sentiment analysis module and stock data analysis)?

