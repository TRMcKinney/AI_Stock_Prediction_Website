import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("Supabase credentials are missing.")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

TABLE_NAME = "prediction_histories"


def insert_predictions(results: dict, latest_close: float) -> None:
    """Insert prediction records for each model."""
    today = datetime.utcnow().date()
    later = today + timedelta(days=10)
    rows = []
    for model, data in results.items():
        if not isinstance(data, dict) or "prediction" not in data:
            continue
        pct = float(data["prediction"])
        predicted_price = round(latest_close * (1 + pct), 2)
        rows.append(
            {
                "date_of_prediction": today.isoformat(),
                "model_type": model,
                "prediction": pct,
                "predicted_price": predicted_price,
                "10_days_later_date": later.isoformat(),
            }
        )
    if rows:
        supabase.table(TABLE_NAME).insert(rows).execute()


def update_with_actual(date: str, close_price: float) -> None:
    """Update rows whose 10 day date matches provided date with actual price."""
    resp = (
        supabase.table(TABLE_NAME)
        .select("id,predicted_price")
        .eq("10_days_later_date", date)
        .is_("actual_price", None)
        .execute()
    )
    for row in resp.data or []:
        diff = close_price - float(row["predicted_price"])
        supabase.table(TABLE_NAME).update(
            {"actual_price": close_price, "difference": diff}
        ).eq("id", row["id"]).execute()


def refresh_missing_actuals() -> int:
    """Populate actual price/difference for past predictions."""
    today = datetime.utcnow().date().isoformat()
    resp = (
        supabase.table(TABLE_NAME)
        .select("id,predicted_price,10_days_later_date")
        .is_("actual_price", None)
        .lte("10_days_later_date", today)
        .execute()
    )

    updated = 0
    for row in resp.data or []:
        date = row["10_days_later_date"]
        price_resp = (
            supabase.table("stock_prices")
            .select("close")
            .eq("timestamp", date)
            .maybe_single()
            .execute()
        )
        if price_resp.data:
            close_price = float(price_resp.data["close"])
            diff = close_price - float(row["predicted_price"])
            supabase.table(TABLE_NAME).update(
                {"actual_price": close_price, "difference": diff}
            ).eq("id", row["id"]).execute()
            updated += 1

    return updated
