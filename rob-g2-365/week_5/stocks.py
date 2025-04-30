RCL = {'name': 'Royal Caribbean', 'symbol': 'RCL'}
CCL = {'name': 'Carnival Cruise', 'symbol': 'CCL'}
NCLH = {'name': 'Norwegian Cruise Line', 'symbol': 'NCLH'}
AWX = {'name':'Avalon Holdings Corporation', 'symbol': 'AWX' }
LIND = {'name': 'Lindblad Expeditions Holdings', 'symbol': 'LIND'}
OSW = {'name': 'OneSpaWorld Holdings', 'symbol': 'OSW'}
WKC = {'name': 'World kinect Corp','symbol': 'WKC'}
QQQ = {'name': 'Nasdaq', 'symbol': 'QQQ'}

STOCKS = [RCL, CCL, NCLH, AWX, LIND, OSW, WKC, QQQ]
COLUMN_NAMES = ['open', 'high', 'low','close', 'volume', 'transactions']

def get_csv_file_name(symbol):
  return f"{symbol}_1min_aggregates.csv"

def get_pkl_file_name(symbol):
  return f"{symbol}_1min_aggregates.pkl"