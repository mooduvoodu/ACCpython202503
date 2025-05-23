import os
from polygon import RESTClient
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
import json
from stocks import *

# Replace with your actual Polygon.io API key
# API_KEY = os.environ.get('POLYGON_API_KEY')
# if not API_KEY:
#     print("Error: Please set the POLYGON_API_KEY environment variable.")
#     exit()
API_KEY =  "dIUMbUHa3jguPZ9WiF5HUgIS4FWhPWlq"
STOCK_TICKER = "AAPL"
TIMESPAN = "minute"
MULTIPLIER = 1
NOW = datetime.now()
TODAY = NOW.strftime("%Y-%m-%d")
START = NOW - relativedelta(months=3)
client = RESTClient(API_KEY)

def get_ticker(symbol, start, end):
  try:
    aggs = []
    for a in client.list_aggs(
      ticker=symbol,
      multiplier=MULTIPLIER,
      timespan=TIMESPAN,
      from_=start,
      to=end,
      limit=50000  # Maximum limit per request
    ):
      aggs.append(a)
  except Exception as e:
    print(f"An error occurred: {e}")    
  return aggs


def get_all_stocks():
  ticker_array = []
  df = pd.DataFrame()
  for stock in STOCKS:
    ticker = get_ticker(stock['symbol'], START, TODAY)
    ticker_df = pd.DataFrame(ticker)
    print(ticker_df.columns)
    ticker_df['datetime'] = pd.to_datetime(ticker_df['timestamp'], unit="ms")
    # optional: set timestamp as index
    ticker_df = ticker_df.set_index('datetime')

    print(ticker_df.columns)
    symbol = stock['symbol']
    pickle_path = get_pkl_file_name(symbol)
    print(pickle_path)
    ticker_df.to_pickle(pickle_path)
    print(f"DataFrame saved to: {pickle_path}")    

    csv_path = get_csv_file_name(symbol)
    ticker_df.to_csv(csv_path)
    print(f"DataFrame saved to: {csv_path}")    
    ticker_array.append( {'symbol':stock['symbol'], 'ticker':ticker_df})

  return df


df = get_all_stocks()
print(df[0].head())
