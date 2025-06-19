import numpy as np
import pandas as pd
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

from baseline_model import compute_features


PARAM_GRID = [
    {"units1": 50, "units2": 20, "epochs": 15},
    {"units1": 100, "units2": 20, "epochs": 25},
    {"units1": 100, "units2": 40, "epochs": 25},
]


def _build_model(input_dim: int, units1: int, units2: int):
    model = Sequential([
        Dense(units1, input_dim=input_dim, activation="relu"),
        Dense(units2, activation="relu"),
        Dense(1, activation="linear"),
    ])
    model.compile(optimizer="adam", loss="mse")
    return model


def train_and_predict(df: pd.DataFrame):
    """Grid search over a small parameter grid and return best metrics."""
    features, targets = compute_features(df)
    scaler = StandardScaler()
    scaled = scaler.fit_transform(features)

    train_size = int(0.85 * len(scaled))
    X_train, X_test = scaled[:train_size], scaled[train_size:]
    y_train, y_test = targets[:train_size], targets[train_size:]

    best_score = -np.inf
    best_model = None
    for params in PARAM_GRID:
        model = _build_model(scaled.shape[1], params["units1"], params["units2"])
        model.fit(X_train, y_train, epochs=params["epochs"], verbose=0)
        preds = model.predict(X_test)
        score = r2_score(y_test, preds)
        if score > best_score:
            best_score = score
            best_model = model

    preds_test = best_model.predict(X_test)
    r2 = r2_score(y_test, preds_test)
    mae = mean_absolute_error(y_test, preds_test)
    rmse = np.sqrt(mean_squared_error(y_test, preds_test))
    latest_pred = best_model.predict(scaled[-1].reshape(1, -1))[0][0]

    return {
        "prediction": float(latest_pred),
        "r2": float(r2),
        "mae": float(mae),
        "rmse": float(rmse),
    }
