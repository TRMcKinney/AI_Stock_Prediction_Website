import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    r2_score,
    mean_absolute_error,
    mean_squared_error,
)
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import matplotlib.pyplot as plt
import io
import base64

# Minimum number of rows required to compute all features. ``rsi200`` needs a
# 200 day window and the model uses a 10-day look-back and 10-day forecast.
MIN_REQUIRED_ROWS = 210


def compute_features(df: pd.DataFrame):
    """Return feature matrix and targets for training."""
    df = df.copy()

    if len(df) < MIN_REQUIRED_ROWS:
        raise ValueError(
            f"Not enough data to compute features — at least {MIN_REQUIRED_ROWS} rows required."
        )

    df["10d_future_close"] = df["close"].shift(-10)
    df["10d_future_close_pct"] = (df["10d_future_close"] - df["close"]) / df[
        "close"
    ]
    df["10d_close_pct"] = df["close"].pct_change(10)

    df["ma14"] = df["close"].rolling(14).mean()
    df["rsi14"] = (
        df["close"].diff().clip(lower=0).rolling(14).mean()
        / df["close"].abs().rolling(14).mean()
    ) * 100

    df["ma30"] = df["close"].rolling(30).mean()
    df["rsi30"] = (
        df["close"].diff().clip(lower=0).rolling(30).mean()
        / df["close"].abs().rolling(30).mean()
    ) * 100

    df["ma50"] = df["close"].rolling(50).mean()
    df["rsi50"] = (
        df["close"].diff().clip(lower=0).rolling(50).mean()
        / df["close"].abs().rolling(50).mean()
    ) * 100

    df["ma200"] = df["close"].rolling(200).mean()
    df["rsi200"] = (
        df["close"].diff().clip(lower=0).rolling(200).mean()
        / df["close"].abs().rolling(200).mean()
    ) * 100

    df = df.dropna()
    if df.empty:
        raise ValueError(
            f"Not enough data to compute features — at least {MIN_REQUIRED_ROWS} rows required."
        )

    features = df[
        [
            "10d_close_pct",
            "ma14",
            "rsi14",
            "ma30",
            "rsi30",
            "ma50",
            "rsi50",
            "ma200",
            "rsi200",
        ]
    ]
    targets = df["10d_future_close_pct"]

    return features, targets

def train_and_predict(df: pd.DataFrame):
    """Train model on historical prices and predict future percentage change."""

    features, targets = compute_features(df)

    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features)

    # Simple chronological train/test split.  Recent data is reserved for
    # evaluating model performance.
    train_size = int(0.85 * len(features))
    X_train, X_test = scaled_features[:train_size], scaled_features[train_size:]
    y_train, y_test = targets[:train_size], targets[train_size:]

    # Basic feed-forward neural network with two hidden layers.  This is a
    # lightweight model intended for demonstration purposes.
    model = Sequential(
        [
            Dense(100, input_dim=X_train.shape[1], activation='relu'),
            Dense(20, activation='relu'),
            Dense(1, activation='linear'),
        ]
    )
    model.compile(optimizer='adam', loss='mse')
    model.fit(X_train, y_train, epochs=25, verbose=0)

    preds_train = model.predict(X_train)
    preds_test = model.predict(X_test)

    # Prediction for the most recent row of data
    latest_input = scaled_features[-1].reshape(1, -1)
    latest_prediction = model.predict(latest_input)[0][0]

    # Visualise how well predictions line up with actual values
    plt.figure()
    plt.scatter(preds_train, y_train, label='train')
    plt.scatter(preds_test, y_test, label='test')
    plt.xlabel("Predicted stock price % change (10 days ahead)")
    plt.ylabel("Actual stock price % change (10 days ahead)")
    plt.legend()
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()

    # === Model evaluation metrics ===
    r2 = r2_score(y_test, preds_test)
    mae = mean_absolute_error(y_test, preds_test)
    try:
        rmse = mean_squared_error(y_test, preds_test, squared=False)
    except TypeError:
        rmse = np.sqrt(mean_squared_error(y_test, preds_test))

    # === Feature importance via permutation ===
    baseline = r2
    importances = []
    for i in range(X_test.shape[1]):
        X_perm = X_test.copy()
        np.random.shuffle(X_perm[:, i])
        perm_preds = model.predict(X_perm)
        score = r2_score(y_test, perm_preds)
        importances.append(baseline - score)

    plt.figure()
    plt.bar(range(len(importances)), importances)
    plt.xticks(range(len(importances)), features.columns, rotation=45, ha='right')
    plt.ylabel('Importance (ΔR²)')
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    importance_base64 = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()

    return {
        "prediction": float(latest_prediction),
        "plot_base64": img_base64,
        "r2": float(r2),
        "mae": float(mae),
        "rmse": float(rmse),
        "importance_plot_base64": importance_base64,
    }
