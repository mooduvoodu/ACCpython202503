import requests
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta

def fetch_1min_aggregates(ticker: str, api_key: str) -> pd.DataFrame:
    """
    Fetch 1-minute aggregate bars for the past 3 months for `ticker`
    from Polygon.io, returning a cleaned DataFrame.
    """
    # 1. Compute date range
    end_dt = datetime.utcnow().date()
    start_dt = (end_dt - relativedelta(months=3))
    start_str = start_dt.strftime("%Y-%m-%d")
    end_str = end_dt.strftime("%Y-%m-%d")

    # 2. Build initial URL and params
    base_url = (
        f"https://api.polygon.io/v2/aggs/ticker/{ticker}/"
        f"range/1/minute/{start_str}/{end_str}"
    )
    params = {
        "adjusted": "true",
        "sort": "asc",
        "limit": 10000,
        "apiKey": api_key
    }

    all_bars = []
    url = base_url
    current_params = params

    # 3. Loop until no more next_url
    while url:
        resp = requests.get(url, params=current_params)
        resp.raise_for_status()
        data = resp.json()

        results = data.get("results", [])
        all_bars.extend(results)

        next_url = data.get("next_url")
        if not next_url:
            break

        # If next_url doesn’t already include your key, append it
        if "apiKey=" not in next_url:
            next_url = f"{next_url}&apiKey={api_key}"

        url = next_url
        current_params = None  # already included in next_url

    # 4. Load into DataFrame and clean up
    df = pd.DataFrame(all_bars)
    if df.empty:
        return df

    # convert epoch ms to datetime
    df["timestamp"] = pd.to_datetime(df["t"], unit="ms")
    df = df.drop(columns=["t"])

    # rename columns for clarity
    df = df.rename(columns={
        "v": "volume",
        "vw": "vwap",
        "o": "open",
        "c": "close",
        "h": "high",
        "l": "low",
        "n": "transaction_count"
    })

    # optional: set timestamp as index
    df = df.set_index("timestamp")

    return df


API_KEY = "dIUMbUHa3jguPZ9WiF5HUgIS4FWhPWlq"
symbol = "AAPL"
df_bars = fetch_1min_aggregates(symbol, API_KEY)
print(df_bars.head())
print(f"\nFetched {len(df_bars)} rows of 1-min bars for {symbol}.")

# 5. Write to pickle
out_dir = "/workspaces/ACCpython202503/assignments"
os.makedirs(out_dir, exist_ok=True)
pickle_path = os.path.join(out_dir, f"{symbol}_1min_aggregates.pkl")
df_bars.to_pickle(pickle_path)
print(f"DataFrame saved to: {pickle_path}")