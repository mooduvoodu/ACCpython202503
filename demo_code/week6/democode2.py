# Install required libraries before running:
# pip install darts[torch] --upgrade

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import requests
import warnings

from darts import TimeSeries
from darts.models import LSTMModel, PatchTSTModel
from darts.dataprocessing.transformers import Scaler
from darts.metrics import mape

warnings.filterwarnings("ignore")

# === Step 1: Fetch 1-minute VWAP data from Polygon.io ===
def fetch_1min_aggregates(ticker: str, api_key: str) -> pd.DataFrame:
    end_dt = datetime.utcnow().date()
    start_dt = end_dt - relativedelta(months=3)
    start_str = start_dt.strftime("%Y-%m-%d")
    end_str = end_dt.strftime("%Y-%m-%d")

    base_url = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/minute/{start_str}/{end_str}"
    params = {
        "adjusted": "true",
        "sort": "asc",
        "limit": 10000,
        "apiKey": api_key
    }

    all_bars = []
    url = base_url
    current_params = params

    while url:
        resp = requests.get(url, params=current_params)
        resp.raise_for_status()
        data = resp.json()
        all_bars.extend(data.get("results", []))
        url = data.get("next_url")
        if url and "apiKey=" not in url:
            url += f"&apiKey={api_key}"
        current_params = None

    df = pd.DataFrame(all_bars)
    if df.empty:
        return df

    df["timestamp"] = pd.to_datetime(df["t"], unit="ms", utc=True).dt.tz_convert("America/New_York")
    df = df.rename(columns={"vw": "vwap"})
    df = df[["timestamp", "vwap"]]
    return df

# === Step 2: Preprocess intraday 1-min series ===
def preprocess_intraday(df: pd.DataFrame) -> pd.DataFrame:
    df = df[df["timestamp"].dt.time >= datetime.strptime("09:30", "%H:%M").time()]
    df = df[df["timestamp"].dt.time < datetime.strptime("16:00", "%H:%M").time()]
    filled = []
    for date, group in df.groupby(df["timestamp"].dt.date):
        start = pd.Timestamp(f"{date} 09:30", tz="America/New_York")
        end = pd.Timestamp(f"{date} 16:00", tz="America/New_York")
        full_index = pd.date_range(start=start, end=end - timedelta(minutes=1), freq="T")
        group = group.set_index("timestamp").reindex(full_index)
        group["vwap"] = group["vwap"].ffill()
        group.index.name = "timestamp"
        filled.append(group)
    df_filled = pd.concat(filled).reset_index()
    return df_filled

# === Step 3: Forecast using LSTM and PatchTST ===

API_KEY = "dIUMbUHa3jguPZ9WiF5HUgIS4FWhPWlq"
SYMBOL = "AAPL"
print("📥 Fetching data...")
raw_df = fetch_1min_aggregates(SYMBOL, API_KEY)
print("🧼 Preprocessing...")
df = preprocess_intraday(raw_df)
df["timestamp"] = df["timestamp"].dt.tz_localize(None)
# Convert to Darts TimeSeries
series = TimeSeries.from_dataframe(df, time_col="timestamp", value_cols="vwap")
# Split last day for validation
split_date = df["timestamp"].dt.date.max()
train = series.drop_after(pd.Timestamp(f"{split_date} 09:29"))
val = series.drop_before(pd.Timestamp(f"{split_date} 09:30"))
# Scale (normalization)
scaler = Scaler()
train_scaled = scaler.fit_transform(train)
val_scaled = scaler.transform(val)
# === LSTM Model ===
lstm = LSTMModel(input_chunk_length=60, output_chunk_length=len(val),
                 hidden_size=64, n_epochs=20, random_state=42, verbose=True)
print("📈 Training LSTM...")
lstm.fit(train_scaled)
print("🔮 Forecasting with LSTM...")
lstm_forecast = lstm.predict(n=len(val))
lstm_forecast = scaler.inverse_transform(lstm_forecast)
# === PatchTST Model ===
patchtst = PatchTSTModel(input_chunk_length=60, output_chunk_length=len(val),
                         patch_len=16, n_epochs=20, random_state=42, verbose=True)
print("📈 Training PatchTST...")
patchtst.fit(train_scaled)
print("🔮 Forecasting with PatchTST...")
patchtst_forecast = patchtst.predict(n=len(val))
patchtst_forecast = scaler.inverse_transform(patchtst_forecast)
# === Evaluation and Plotting ===
print("📊 Plotting results...")
val.plot(label="Actual")
lstm_forecast.plot(label="LSTM Forecast")
patchtst_forecast.plot(label="PatchTST Forecast")
plt.title("1-Minute VWAP Forecast for Next Trading Day")
plt.legend()
plt.show()
print(f"LSTM MAPE: {mape(val, lstm_forecast):.2f}%")
print(f"PatchTST MAPE: {mape(val, patchtst_forecast):.2f}%")


