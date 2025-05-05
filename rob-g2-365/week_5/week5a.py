#    Polygon key :  	dIUMbUHa3jguPZ9WiF5HUgIS4FWhPWlq
#   Write code to pull down on active stock tickers at  https://polygon.io/docs/rest/stocks/tickers/all-tickers
# use just use market type of stocks
# install the polygon python api libraryies:  pip install -U polygon-api-client

import os
import requests
import pandas as pd
from urllib.parse import urlencode

# ------------------------------------------------------------------
# 1. Configuration
# ------------------------------------------------------------------
API_KEY =  "dIUMbUHa3jguPZ9WiF5HUgIS4FWhPWlq"
BASE_URL = "https://api.polygon.io/v3/reference/tickers"

# Query parameters for the *first* call
params = {
    "market": "stocks",
    "active": "true",
    "order": "asc",
    "limit": 1000,  
    "type": "",            # Polygon allows up to 1000 per page
    "sort": "ticker",
    "apiKey": API_KEY        # always include your key
}

# ------------------------------------------------------------------
# 2. Helper: add the apiKey back to every next_url
# ------------------------------------------------------------------
def attach_key(url: str, key: str) -> str:
    """Polygon's `next_url` omits the apiKey – keep adding it."""
    separator = "&" if "?" in url else "?"
    return f"{url}{separator}apiKey={key}"

# ------------------------------------------------------------------
# 3. Page-through loop
# ------------------------------------------------------------------
all_tickers = []          # where we'll collect every record
url = f"{BASE_URL}?{urlencode(params)}"

while url:
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()             # raises if HTTP error

    payload = resp.json()               # -> dict
    all_tickers.extend(payload.get("results", []))

    # Move to the next page (if any)
    url = payload.get("next_url")
    if url:
        url = attach_key(url, API_KEY)

# ------------------------------------------------------------------
# 4. Load into pandas
# ------------------------------------------------------------------
df = pd.DataFrame(all_tickers)

# quick sanity checks
print(df.head())
print(f"\nTotal tickers retrieved: {len(df):,}")

display(df)



# get time series aggregate for stock data over the last few months with 1 minute aggr

# next file week5b.py

