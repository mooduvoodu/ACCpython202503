# Stock 1‑Minute VWAP Forecasting with LSTM & Transformer
# -----------------------------------------------------------------------------
# Key improvements (May 2025)
# • Flexible pre‑processing that handles irregular gaps, market‑closed periods,   
#   and optional extended hours (04:00–20:00 ET).
# • Two CSVs written: forecasts + per‑model validation metrics.
# • Choice of gap‑filling method: forward‑fill or linear interpolation.
# -----------------------------------------------------------------------------

# Installation (if needed):
#   pip install torch pandas numpy matplotlib scikit-learn requests python-dateutil

import pandas as pd
import numpy as np
import requests
import matplotlib.pyplot as plt
from datetime import datetime, timedelta, time
from dateutil.relativedelta import relativedelta
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_absolute_error

import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader

# ============================ CONFIGURATION ==================================
API_KEY         = "dIUMbUHa3jguPZ9WiF5HUgIS4FWhPWlq"  # 🔑 <–– replace with env var in prod
TICKER          = "AAPL"
INCLUDE_EXT_HRS = True       # True = 04:00–20:00 ET, False = 09:30–16:00 ET
FILL_METHOD     = "interpolate"  # "ffill" | "interpolate"
INPUT_LEN       = 450       # look‑back window (minutes)
EPOCHS          = 2
BATCH_SIZE      = 32
DEVICE          = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# =============================================================================

# --------------------------- DATA INGESTION ----------------------------------
def fetch_last_3m(ticker: str, api_key: str) -> pd.DataFrame:
    """Pull the last ~3 months of one‑minute bars from Polygon.io (adjusted)."""
    end_dt   = datetime.utcnow().date()
    start_dt = end_dt - relativedelta(months=3)

    base_url = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/minute/{start_dt}/{end_dt}"
    params   = {"adjusted": "true", "sort": "asc", "limit": 50000, "apiKey": api_key}
    all_rows, url, param_stack = [], base_url, params

    while url:
        r = requests.get(url, params=param_stack)
        r.raise_for_status()
        payload = r.json()
        all_rows.extend(payload.get("results", []))
        url = payload.get("next_url")
        if url and "apiKey=" not in url:
            url += f"&apiKey={api_key}"
        param_stack = None  # only for first call

    df = pd.DataFrame(all_rows)
    if df.empty:
        raise ValueError("No data returned from Polygon API – check symbol or API key")

    # Convert ms‑epoch to timezone‑aware timestamp then to naive ET
    df["timestamp"] = pd.to_datetime(df["t"], unit="ms", utc=True).dt.tz_convert("America/New_York")
    df["timestamp"] = df["timestamp"].dt.tz_localize(None)

    df = df.rename(columns={"vw": "vwap"})
    return df[["timestamp", "vwap"]]

# ----------------------------- PRE‑PROCESS -----------------------------------
REG_START, REG_END = time(9, 30), time(16, 0)
EXT_START, EXT_END = time(4, 0), time(20, 0)
REG_MINUTES        = int(((datetime.combine(datetime.min, REG_END) -
                           datetime.combine(datetime.min, REG_START)).total_seconds()) // 60)
EXT_MINUTES        = int(((datetime.combine(datetime.min, EXT_END) -
                           datetime.combine(datetime.min, EXT_START)).total_seconds()) // 60)

def preprocess(df: pd.DataFrame, include_ext: bool = False, fill_method: str = "ffill") -> pd.DataFrame:
    """Return a gap‑free minute‑level VWAP series for each trading day.

    include_ext : If True, keeps 04:00–20:00 ET; else 09:30–16:00 ET.
    fill_method  : "ffill" simply carries last value forward; "interpolate" uses
                   linear interpolation first, then forward/back‑fill for edges."""
    start_t, end_t = (EXT_START, EXT_END) if include_ext else (REG_START, REG_END)

    processed_days = []
    for d, grp in df.groupby(df["timestamp"].dt.date):
        # Filter to desired session
        mask = (grp["timestamp"].dt.time >= start_t) & (grp["timestamp"].dt.time < end_t)
        grp  = grp[mask]
        if grp.empty:
            continue

        minute_index = pd.date_range(start=datetime.combine(d, start_t),
                                     end=datetime.combine(d, end_t) - timedelta(minutes=1),
                                     freq="T")
        grp = grp.set_index("timestamp").reindex(minute_index)

        if fill_method == "interpolate":
            grp["vwap"] = grp["vwap"].interpolate(limit_direction="both")
        else:  # ffill/bfill combo
            grp["vwap"] = grp["vwap"].ffill().bfill()

        grp.index.name = "timestamp"
        processed_days.append(grp)

    return pd.concat(processed_days).reset_index()

# ----------------------- TORCH DATASET & MODELS ------------------------------
class MinuteDataset(Dataset):
    def __init__(self, series: np.ndarray, in_len: int, out_len: int):
        self.series = series
        self.in_len = in_len
        self.out_len = out_len

    def __len__(self):
        return len(self.series) - self.in_len - self.out_len

    def __getitem__(self, idx):
        x = self.series[idx : idx + self.in_len]
        y = self.series[idx + self.in_len : idx + self.in_len + self.out_len]
        return torch.tensor(x, dtype=torch.float32), torch.tensor(y, dtype=torch.float32)

class LSTMModel(nn.Module):
    def __init__(self, hidden=64, out_len=REG_MINUTES):
        super().__init__()
        self.lstm  = nn.LSTM(input_size=1, hidden_size=hidden, num_layers=2, batch_first=True)
        self.fc    = nn.Linear(hidden, out_len)

    def forward(self, x):  # x: (B, T, 1)
        h, _ = self.lstm(x)
        out  = self.fc(h[:, -1, :])
        return out.unsqueeze(-1)  # (B, out_len, 1)

class TransformerModel(nn.Module):
    def __init__(self, in_len: int, out_len: int, d_model=64, nhead=4, nlayers=2):
        super().__init__()
        self.linear_in    = nn.Linear(1, d_model)
        self.pos_embed    = nn.Parameter(torch.randn(1, in_len, d_model))
        enc_layer         = nn.TransformerEncoderLayer(d_model=d_model, nhead=nhead, batch_first=True)
        self.encoder      = nn.TransformerEncoder(enc_layer, num_layers=nlayers)
        self.linear_out   = nn.Linear(d_model, out_len)

    def forward(self, x):
        x = self.linear_in(x) + self.pos_embed
        x = self.encoder(x)
        x = self.linear_out(x[:, -1, :])
        return x.unsqueeze(-1)

# ---------------------------- TRAINING UTIL ----------------------------------
def train(model, loader, epochs=10, lr=1e-3):
    model.to(DEVICE)
    loss_fn   = nn.MSELoss()
    optim     = torch.optim.Adam(model.parameters(), lr=lr)
    for ep in range(1, epochs + 1):
        model.train()
        epoch_loss = 0.0
        for xb, yb in loader:
            xb = xb.unsqueeze(-1).to(DEVICE)
            yb = yb.to(DEVICE)
            pred = model(xb)
            loss = loss_fn(pred.squeeze(), yb.squeeze())
            optim.zero_grad()
            loss.backward()
            optim.step()
            epoch_loss += loss.item()
        print(f"Epoch {ep:02d}/{epochs} | Loss: {epoch_loss / len(loader):.6f}")

@torch.no_grad()
def infer(model, last_seq: np.ndarray, scaler: MinMaxScaler) -> np.ndarray:
    model.eval()
    x = torch.tensor(last_seq, dtype=torch.float32).unsqueeze(0).unsqueeze(-1).to(DEVICE)
    y = model(x).cpu().squeeze().numpy()
    return scaler.inverse_transform(y.reshape(-1, 1)).flatten()

# ----------------------------- MAIN PIPELINE ---------------------------------

def mape(a, f):
    return np.mean(np.abs((a - f) / a)) * 100


def run_pipeline():
    print("→ Fetching data …")
    raw_df = fetch_last_3m(TICKER, API_KEY)

    print("→ Pre‑processing …")
    clean_df = preprocess(raw_df, include_ext=INCLUDE_EXT_HRS, fill_method=FILL_METHOD)

    # Determine training vs test (last day held‑out)
    last_day  = clean_df["timestamp"].dt.date.max()
    train_ser = clean_df[clean_df["timestamp"].dt.date < last_day]["vwap"].values
    test_ser  = clean_df[clean_df["timestamp"].dt.date == last_day]["vwap"].values

    out_len   = EXT_MINUTES if INCLUDE_EXT_HRS else REG_MINUTES
    if len(test_ser) != out_len:
        # Clip/pad to expected length
        if len(test_ser) > out_len:
            test_ser = test_ser[:out_len]
        else:
            test_ser = np.pad(test_ser, (0, out_len - len(test_ser)), constant_values=test_ser[-1])

    # Scaling
    scaler       = MinMaxScaler()
    train_scaled = scaler.fit_transform(train_ser.reshape(-1, 1)).flatten()

    ds      = MinuteDataset(train_scaled, INPUT_LEN, out_len)
    loader  = DataLoader(ds, batch_size=BATCH_SIZE, shuffle=True)

    # ---------- LSTM ----------
    print("→ Training LSTM …")
    lstm = LSTMModel(out_len=out_len)
    train(lstm, loader, epochs=EPOCHS)
    lstm_fore = infer(lstm, train_scaled[-INPUT_LEN:], scaler)

    # ---------- Transformer ----------
    print("→ Training Transformer …")
    trf = TransformerModel(INPUT_LEN, out_len)
    train(trf, loader, epochs=EPOCHS)
    trf_fore = infer(trf, train_scaled[-INPUT_LEN:], scaler)

    # ---------- Validation ----------
    lstm_mae = mean_absolute_error(test_ser, lstm_fore)
    trf_mae  = mean_absolute_error(test_ser, trf_fore)
    lstm_mp  = mape(test_ser, lstm_fore)
    trf_mp   = mape(test_ser, trf_fore)

    # ---------- CSV OUTPUT ----------
    print("→ Writing CSVs …")
    day_df = clean_df[clean_df["timestamp"].dt.date == last_day].copy().reset_index(drop=True)
    day_df = day_df.iloc[:out_len]
    day_df["actual_vwap"]  = test_ser
    day_df["lstm_forecast"] = lstm_fore
    day_df["trf_forecast"]  = trf_fore
    day_df.to_csv("vwap_forecast_output.csv", index=False)

    metrics_df = pd.DataFrame({
        "model": ["LSTM", "Transformer"],
        "MAE"  : [lstm_mae, trf_mae],
        "MAPE" : [lstm_mp,  trf_mp]
    })
    metrics_df.to_csv("vwap_validation_scores.csv", index=False)

    # ---------- Plot ----------
    plt.figure(figsize=(13, 6))
    plt.plot(test_ser, label="Actual", linewidth=2)
    plt.plot(lstm_fore, label="LSTM")
    plt.plot(trf_fore, label="Transformer")
    plt.title(f"{TICKER} VWAP Forecast (Held‑Out {last_day})")
    plt.xlabel("Minute of Session")
    plt.ylabel("VWAP")
    plt.legend(); plt.grid(True); plt.tight_layout(); plt.show()

    print("✔ Done – CSVs saved & chart displayed.")

# ----------------------------- ENTRYPOINT ------------------------------------

run_pipeline()
