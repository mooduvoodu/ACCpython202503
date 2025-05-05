# Write in your folder that will save all active tickers (ticker Polygon API) all under
# Stock REST DOCS...save in your folder as pickel
# Then write code that will
# Take 8 stocks under CS (common) and/or ETF types. Create the dataframe from the Polygon API call. 1 minute agg.
# Last 3 months of historicals from the time you run the code. Save each stock as it's own pickel or all in one big pickel.

import requests
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta

def fetch_1min_aggregates(ticker: str, api_key: str) -> pd.DataFrame:
    end_dt = datetime.utcnow().date()
    start_dt = (end_dt - relativedelta(months=3))
    start_str = start_dt.strftime("%Y-%m-%d")
    end_str = end_dt.strftime("%Y-%m-%d")

    base_url = (
        f"https://api.polygon.io/v2/aggs/ticker/{ticker}/"
        f"range/1/minute/{start_str}/{end_str}")
    params = {
        "adjusted": "true",
        "sort": "asc",
        "limit": 10000,
        "apiKey": api_key}
    all_bars = []
    url = base_url
    current_params = params

    while url:
        resp = requests.get(url, params=current_params)
        resp.raise_for_status()
        data = resp.json()

        results = data.get("results", [])
        all_bars.extend(results)

        next_url = data.get("next_url")
        if not next_url:
            break

        if "apiKey=" not in next_url:
            next_url = f"{next_url}&apiKey={api_key}"

        url = next_url
        current_params = None

        df = pd.DataFrame(all_bars)
        if df.empty:
            return df
        
        df["timestamp"] = pd.to_datetime(df["t"], unit="ms")
        df = df.drop(columns=["t"])

        df = df.rename(columns={
        "v": "volume",
        "vw": "vwap",
        "o": "open",
        "c": "close",
        "h": "high",
        "l": "low",
        "n": "transaction_count"})

        df = df.set_index("timestamp")

        return df
    
API_KEY = "dIUMbUHa3jguPZ9WiF5HUgIS4FWhPWlq"
symbol = "NFLX"
df_bars = fetch_1min_aggregates(symbol, API_KEY)
print(df_bars.head())
print(f"\nFetched {len(df_bars)} rows of 1-min bars for {symbol}.")

out_dir = "/workspaces/ACCpython202503/bsistrunk/pickle_files"
os.makedirs(out_dir, exist_ok=True)
pickle_path = os.path.join(out_dir, f"{symbol}_1min_aggregates.pkl")
df_bars.to_pickle(pickle_path)
print(f"DataFrame saved to: {pickle_path}")