import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import matplotlib.pyplot as plt
import io
import base64

def train_and_predict(df: pd.DataFrame):
    df = df.copy()
    df['10d_future_close'] = df['close'].shift(-10)
    df['10d_future_close_pct'] = df['10d_future_close'].pct_change(10)
    df['10d_close_pct'] = df['close'].pct_change(10)

    df['ma14'] = df['close'].rolling(14).mean()
    df['rsi14'] = (df['close'].diff().clip(lower=0).rolling(14).mean() /
                   df['close'].abs().rolling(14).mean()) * 100

    df['ma30'] = df['close'].rolling(30).mean()
    df['rsi30'] = (df['close'].diff().clip(lower=0).rolling(30).mean() /
                   df['close'].abs().rolling(30).mean()) * 100

    df['ma50'] = df['close'].rolling(50).mean()
    df['rsi50'] = (df['close'].diff().clip(lower=0).rolling(50).mean() /
                   df['close'].abs().rolling(50).mean()) * 100

    df['ma200'] = df['close'].rolling(200).mean()
    df['rsi200'] = (df['close'].diff().clip(lower=0).rolling(200).mean() /
                    df['close'].abs().rolling(200).mean()) * 100

    df = df.dropna()
    if df.empty:
        raise ValueError("Not enough data to compute features — at least 200 rows required.")

    features = df[['10d_close_pct', 'ma14', 'rsi14', 'ma30', 'rsi30', 'ma50', 'rsi50', 'ma200', 'rsi200']]
    targets = df['10d_future_close_pct']

    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features)

    train_size = int(0.85 * len(df))
    X_train, X_test = scaled_features[:train_size], scaled_features[train_size:]
    y_train, y_test = targets[:train_size], targets[train_size:]

    model = Sequential([
        Dense(100, input_dim=X_train.shape[1], activation='relu'),
        Dense(20, activation='relu'),
        Dense(1, activation='linear')
    ])
    model.compile(optimizer='adam', loss='mse')
    model.fit(X_train, y_train, epochs=25, verbose=0)

    preds_train = model.predict(X_train)
    preds_test = model.predict(X_test)

    # Latest prediction
    latest_input = scaled_features[-1].reshape(1, -1)
    latest_prediction = model.predict(latest_input)[0][0]

    # Plot
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

    return {
        "prediction": latest_prediction,
        "plot_base64": img_base64
    }