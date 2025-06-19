"""Model that persists its weights to Supabase."""

import base64
import io
import os
import pickle
import tempfile

import numpy as np
import pandas as pd
from dotenv import load_dotenv
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense
from supabase import create_client

from baseline_model import compute_features

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("Supabase credentials are missing.")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

TABLE_NAME = "persistence_model"


def _build_model(input_dim: int):
    model = Sequential([
        Dense(100, input_dim=input_dim, activation="relu"),
        Dense(20, activation="relu"),
        Dense(1, activation="linear"),
    ])
    model.compile(optimizer="adam", loss="mse")
    return model


def _load_persisted():
    """Return persisted (model, scaler) from Supabase or (None, None)."""
    resp = (
        supabase.table(TABLE_NAME)
        .select("model", "scaler")
        .maybe_single()
        .execute()
    )
    if resp and resp.data:
        model_bytes = base64.b64decode(resp.data["model"])
        scaler_bytes = base64.b64decode(resp.data["scaler"])
        scaler = pickle.loads(scaler_bytes)
        with tempfile.NamedTemporaryFile(suffix=".keras", delete=False) as tmp:
            tmp.write(model_bytes)
            tmp.flush()
            model = load_model(tmp.name)
        os.unlink(tmp.name)
        return model, scaler
    return None, None


def _persist(model, scaler):
    scaler_b64 = base64.b64encode(pickle.dumps(scaler)).decode()
    with tempfile.NamedTemporaryFile(suffix=".keras", delete=False) as tmp:
        model.save(tmp.name)
        tmp.seek(0)
        model_b64 = base64.b64encode(tmp.read()).decode()
    os.unlink(tmp.name)

    existing = (
        supabase.table(TABLE_NAME).select("id").eq("id", 1).maybe_single().execute()
    )
    if existing and existing.data:
        supabase.table(TABLE_NAME).update(
            {"model": model_b64, "scaler": scaler_b64}
        ).eq("id", 1).execute()
    else:
        supabase.table(TABLE_NAME).insert(
            {"id": 1, "model": model_b64, "scaler": scaler_b64}
        ).execute()


def train_and_predict(df: pd.DataFrame):
    """Use a persisted model if available; otherwise train and save it."""
    features, targets = compute_features(df)

    model, scaler = _load_persisted()

    if model and scaler:
        scaled = scaler.transform(features)
    else:
        scaler = StandardScaler()
        scaled = scaler.fit_transform(features)
        model = _build_model(scaled.shape[1])
        model.fit(scaled, targets, epochs=25, verbose=0)
        _persist(model, scaler)

    train_size = int(0.85 * len(scaled))
    X_test = scaled[train_size:]
    y_test = targets[train_size:]
    preds_test = model.predict(X_test)
    r2 = r2_score(y_test, preds_test)
    mae = mean_absolute_error(y_test, preds_test)
    rmse = np.sqrt(mean_squared_error(y_test, preds_test))

    latest_pred = model.predict(scaled[-1].reshape(1, -1))[0][0]

    return {
        "prediction": float(latest_pred),
        "r2": float(r2),
        "mae": float(mae),
        "rmse": float(rmse),
    }
