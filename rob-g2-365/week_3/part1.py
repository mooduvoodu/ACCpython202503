import pandas as pd
from file_paths import *


# Part 1 Import & Profile
def show_data_frame(df):
  print(f"Shape:\n{df.shape} \n")
  print(f"Columns:\n{df.columns} \n")
  print(f"dtypes:\n{df.dtypes}\n")
  print(f"head:\n{df.head()}\n")
  print(f"info:\n{df.info()}\n")
  print(f"describe:\n{df.describe()}\n")

for file in CSV_FILES:
  df = pd.read_csv(str(file), sep='|', encoding='latin-1')
  show_data_frame(df)



