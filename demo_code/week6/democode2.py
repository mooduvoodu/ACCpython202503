# Install required packages before running (if not already installed):
# pip install torch pandas matplotlib scikit-learn requests

import pandas as pd
import numpy as np
import requests
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from sklearn.preprocessing import MinMaxScaler

import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader

# ==== Fetch Data ====
def fetch_1min_vwap(ticker: str, api_key: str) -> pd.DataFrame:
    end_dt = datetime.utcnow().date()
    start_dt = end_dt - relativedelta(months=3)
    base_url = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/minute/{start_dt}/{end_dt}"
    params = {"adjusted": "true", "sort": "asc", "limit": 10000, "apiKey": api_key}
    all_bars, url, current_params = [], base_url, params

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
    df["timestamp"] = pd.to_datetime(df["t"], unit="ms", utc=True).dt.tz_convert("America/New_York")
    df = df.rename(columns={"vw": "vwap"})
    return df[["timestamp", "vwap"]]

# ==== Preprocess ====
def preprocess(df):
    df = df[df["timestamp"].dt.time >= datetime.strptime("09:30", "%H:%M").time()]
    df = df[df["timestamp"].dt.time < datetime.strptime("16:00", "%H:%M").time()]
    df["timestamp"] = df["timestamp"].dt.tz_localize(None)
    all_days = []
    for date, group in df.groupby(df["timestamp"].dt.date):
        start = pd.Timestamp(f"{date} 09:30")
        end = pd.Timestamp(f"{date} 16:00")
        minutes = pd.date_range(start=start, end=end - timedelta(minutes=1), freq="T")
        group = group.set_index("timestamp").reindex(minutes)
        group["vwap"] = group["vwap"].ffill()
        group.index.name = "timestamp"
        all_days.append(group)
    return pd.concat(all_days).reset_index()

# ==== PyTorch Dataset ====
class TimeSeriesDataset(Dataset):
    def __init__(self, data, input_len, output_len):
        self.data = data
        self.input_len = input_len
        self.output_len = output_len

    def __len__(self):
        return len(self.data) - self.input_len - self.output_len

    def __getitem__(self, i):
        x = self.data[i:i+self.input_len]
        y = self.data[i+self.input_len:i+self.input_len+self.output_len]
        return torch.tensor(x, dtype=torch.float32), torch.tensor(y, dtype=torch.float32)

# ==== LSTM ====
class LSTMModel(nn.Module):
    def __init__(self, input_size=1, hidden_size=64, output_len=390):
        super().__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, batch_first=True, num_layers=2)
        self.linear = nn.Linear(hidden_size, output_len)

    def forward(self, x):
        out, _ = self.lstm(x)
        out = self.linear(out[:, -1, :])
        return out.unsqueeze(-1)

# ==== Transformer ====
class TransformerModel(nn.Module):
    def __init__(self, input_len, output_len, d_model=64, nhead=4, num_layers=2):
        super().__init__()
        self.input_proj = nn.Linear(1, d_model)
        self.pos_embedding = nn.Parameter(torch.randn(1, input_len, d_model))
        encoder_layer = nn.TransformerEncoderLayer(d_model=d_model, nhead=nhead, batch_first=True)
        self.encoder = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)
        self.output_proj = nn.Linear(d_model, output_len)

    def forward(self, x):
        x = self.input_proj(x) + self.pos_embedding
        x = self.encoder(x)
        x = self.output_proj(x[:, -1, :])
        return x.unsqueeze(-1)

# ==== Train Loop ====
def train(model, dataloader, epochs=10, lr=1e-3):
    model.to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    loss_fn = nn.MSELoss()
    for epoch in range(epochs):
        model.train()
        total_loss = 0
        for xb, yb in dataloader:
            xb, yb = xb.unsqueeze(-1).to(device), yb.to(device)
            pred = model(xb)
            loss = loss_fn(pred.squeeze(), yb.squeeze())
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
        print(f"Epoch {epoch+1}/{epochs}, Loss: {total_loss/len(dataloader):.4f}")

# ==== Forecast ====
def forecast(model, last_sequence, scaler):
    model.eval()
    with torch.no_grad():
        x = torch.tensor(last_sequence, dtype=torch.float32).unsqueeze(0).unsqueeze(-1).to(device)
        yhat = model(x).cpu().squeeze().numpy()
        return scaler.inverse_transform(yhat.reshape(-1, 1)).flatten()

# ==== Main Runner ====
def run():
    # Settings
    input_len = 60
    output_len = 390  # full trading day
    epochs = 10

    # Fetch & preprocess
    api_key = "dIUMbUHa3jguPZ9WiF5HUgIS4FWhPWlq"
    df = fetch_1min_vwap("AAPL", api_key)
    df = preprocess(df)

    last_day = df["timestamp"].dt.date.max()
    train_data = df[df["timestamp"].dt.date < last_day]["vwap"].values
    test_data = df[df["timestamp"].dt.date == last_day]["vwap"].values

    # Normalize
    scaler = MinMaxScaler()
    train_scaled = scaler.fit_transform(train_data.reshape(-1, 1)).flatten()

    # Dataset
    dataset = TimeSeriesDataset(train_scaled, input_len, output_len)
    loader = DataLoader(dataset, batch_size=32, shuffle=True)

    # LSTM
    print("Training LSTM...")
    lstm = LSTMModel(output_len=output_len)
    train(lstm, loader, epochs)
    lstm_forecast = forecast(lstm, train_scaled[-input_len:], scaler)

    # Transformer
    print("Training Transformer...")
    transformer = TransformerModel(input_len, output_len)
    train(transformer, loader, epochs)
    transformer_forecast = forecast(transformer, train_scaled[-input_len:], scaler)

    # Plot
    plt.figure(figsize=(12, 6))
    plt.plot(test_data, label="Actual")
    plt.plot(lstm_forecast, label="LSTM")
    plt.plot(transformer_forecast, label="Transformer")
    plt.legend()
    plt.title("1-Minute VWAP Forecast - LSTM vs Transformer")
    plt.xlabel("Minute")
    plt.ylabel("VWAP")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# ==== Device ====
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Run it
run()
