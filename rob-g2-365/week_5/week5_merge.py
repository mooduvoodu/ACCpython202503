import pandas as pd
from stocks import *

def merge_files_for_stock(symbol, merge_dict, df):
  for column_name in COLUMN_NAMES:
    df_new = df[['datetime', column_name]]
    df_new = df_new.set_index('datetime')

    df_new = df_new.rename(columns={column_name: symbol})
    # print(df_new.columns)
    # print(df_new.head())

    merge_dict[column_name] = pd.merge(merge_dict[column_name], df_new, left_index=True, right_index = True, how='outer')
    df_merge = merge_dict[column_name]
    # print(df_merge.columns)
    # print(df_merge.head())

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

dict = create_merge_dict()
print(dict.keys())
first_df = list(dict.values())[0]
print(type(first_df))
print(first_df.columns)
write_merge_dict_to_files(dict)
