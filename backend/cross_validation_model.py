import numpy as np
import pandas as pd
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from sklearn.model_selection import TimeSeriesSplit
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

from baseline_model import compute_features


def train_and_predict(df: pd.DataFrame):
    """Train using cross validation and return average metrics."""
    features, targets = compute_features(df)

    scaler = StandardScaler()
    scaled = scaler.fit_transform(features)

    tss = TimeSeriesSplit(n_splits=5)
    r2_scores = []
    mae_scores = []
    rmse_scores = []
    for train_idx, test_idx in tss.split(scaled):
        X_train, X_test = scaled[train_idx], scaled[test_idx]
        y_train, y_test = targets.iloc[train_idx], targets.iloc[test_idx]

        model = Sequential([
            Dense(100, input_dim=X_train.shape[1], activation="relu"),
            Dense(20, activation="relu"),
            Dense(1, activation="linear"),
        ])
        model.compile(optimizer="adam", loss="mse")
        model.fit(X_train, y_train, epochs=25, verbose=0)

        preds = model.predict(X_test)
        r2_scores.append(r2_score(y_test, preds))
        mae_scores.append(mean_absolute_error(y_test, preds))
        rmse_scores.append(np.sqrt(mean_squared_error(y_test, preds)))

    # Train on full data for final prediction
    final_model = Sequential([
        Dense(100, input_dim=scaled.shape[1], activation="relu"),
        Dense(20, activation="relu"),
        Dense(1, activation="linear"),
    ])
    final_model.compile(optimizer="adam", loss="mse")
    final_model.fit(scaled, targets, epochs=25, verbose=0)
    latest_pred = final_model.predict(scaled[-1].reshape(1, -1))[0][0]

    return {
        "prediction": float(latest_pred),
        "r2": float(np.mean(r2_scores)),
        "mae": float(np.mean(mae_scores)),
        "rmse": float(np.mean(rmse_scores)),
    }
