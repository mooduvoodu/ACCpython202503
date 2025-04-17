import pandas as pd

#================================================================
#1. Load the dataset from the provided pipe-delimited CSV file
#================================================================
data_url = '/workspaces/ACCpython202503/datasets/orderdetails.csv'
df = pd.read_csv(data_url, delimiter='|')

#Check column names to confirm
print("Column Names:", df.columns.tolist())



#================================================================
# 2. Data Exploration Basics
#================================================================