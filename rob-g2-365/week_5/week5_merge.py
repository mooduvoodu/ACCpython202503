import pandas as pd
import math
from stocks import *
import re
import matplotlib.pyplot as plt

def merge_files_for_stock(symbol, merge_dict, df):
  for column_name in COLUMN_NAMES:
    df_new = df[['datetime', column_name]]
    df_new = df_new.set_index('datetime')

    df_new = df_new.rename(columns={column_name: symbol})

    merge_dict[column_name] = pd.merge(merge_dict[column_name], df_new, left_index=True, right_index = True, how='outer')
    df_merge = merge_dict[column_name]

def create_dict_of_empty_dataframes():
  df_dict = {}
  for symbol in COLUMN_NAMES:
    df_dict[symbol]=pd.DataFrame()
  return df_dict

def create_merge_dict():
  merge_dict = create_dict_of_empty_dataframes()
  for stock in STOCKS:
    symbol = stock['symbol']
    filename =get_csv_file_name(symbol)
    df = pd.read_csv(filename)
    merge_files_for_stock(symbol, merge_dict, df)

  return merge_dict

def write_merge_dict_to_files(merge_dict):
  for symbol, df in merge_dict.items():
    df.to_csv(symbol + '.csv')

def calculate_total_volume_and_trades():
  df_totals = pd.DataFrame(columns=['symbol', 'total_transactions', 'total_volume'])
  df_totals.set_index('symbol', inplace=True)
  for stock in STOCKS:
    symbol = stock['symbol']
    filename =get_csv_file_name(symbol)
    df = pd.read_csv(filename)
    total_transactions = df['transactions'].sum()
    total_volume = df['volume'].sum()

    df_totals.loc[symbol] = {'symbol':symbol, 'total_transactions': total_transactions, 'total_volume':total_volume}
  df_totals.to_csv('totals.csv')    

def create_ideal_benford_subdataframe():
  df = pd.DataFrame(columns=['number', 'ideal'])  
  df.set_index('number', inplace=True)
  for n in range(1,10):
    df.loc[n, 'ideal'] = math.log10(n+1) - math.log10(n)
  return df

def get_leading_digit(value):
  return int(str(value)[0])

def create_benford_subdataframe(df, symbol, column_name):
  new_col = symbol + '_' + column_name
  df_new = pd.DataFrame(columns=['number', new_col])  
  df_new['number'] = range(1, 10)
  # df_new['number'] =  df_new['number'].astype(int)
  df_new.set_index(['number'], inplace=True)
  leading_digits = df[column_name].astype(str).str[0]
  digit_counts = leading_digits.value_counts().sort_index()
  for n in range(1,10):
    df_new.loc[n, new_col] = digit_counts[f"{n}"] / len(df)
  return df_new



def benfords_law_on_volume_and_transactions():
  df_benford = pd.DataFrame(columns=['number'])
  df_benford.set_index(['number'], inplace=True)
  subframe = create_ideal_benford_subdataframe()
  df_benford = pd.merge(df_benford, subframe, on='number', how='outer')
  for stock in STOCKS:
    symbol = stock['symbol']
    filename =get_csv_file_name(symbol)
    df = pd.read_csv(filename)
    subframe = create_benford_subdataframe(df, symbol, 'volume')
    df_benford = pd.merge(df_benford, subframe, on='number', how='outer')
  return df_benford


#dict = create_merge_dict()
#print(dict.keys())
#first_df = list(dict.values())[0]
#print(type(first_df))
#print(first_df.columns)
#write_merge_dict_to_files(dict)

# calculate_total_volume_and_trades()
# df = create_ideal_benford_subdataframe()
# print(df)

#filename =get_csv_file_name('QQQ')
#df = pd.read_csv(filename)
#ben_df = create_benford_subdataframe(df, 'QQQ', 'volume')
#print(ben_df)

df = benfords_law_on_volume_and_transactions()
#print(df)
print(df.columns)
#df.set_index('number')
#df.reset_index()
# print(df['number'].dtype)
# df['number'] = df['number'].astype(int)
# df.plot(x='number', y='ideal', kind='bar', color='skyblue', edgecolor='black')
# plt.show()

# plt.figure(figsize=(8, 6)) # Optional: Adjust figure size
df[['ideal', 'QQQ_volume']].plot(kind='bar')
plt.xlabel('Number')
plt.ylabel('Ideal Value')
plt.title('Bar Plot of Ideal Values')
plt.xticks(rotation=0) # Keep x-axis labels horizontal
plt.grid(axis='y', linestyle='--') # Optional: Add a horizontal grid
plt.tight_layout() # Adjust layout to prevent labels from overlapping
plt.show()
