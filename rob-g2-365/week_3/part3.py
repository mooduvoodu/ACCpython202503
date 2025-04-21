from file_paths import *
import pandas as pd

# Part 3: Boolean Row Filtering
#   3.1 Customers
#      • FirstName startswith A or J
#      • MiddleName is not null
#      • FirstName contains 'ar' (case‑insensitive)
#      • Title not in ['Mr.','Ms.']

df = pd.read_csv(CUSTOMER_PATH, sep='|', encoding='latin-1')
df = df[['FirstName','MiddleName','Title']]
print(df.loc[(df['FirstName'].str[0] == 'A') | (df['FirstName'].str[0] == 'J') ])
print(df.loc[(df['MiddleName'].str[0] != None) &  (df['MiddleName'].str[0] != '') &  ~pd.isna(df['MiddleName'])])
print(df.loc[df['FirstName'].str.lower().str.contains('ar')])
print(df.loc[(df['Title'] == 'Mr.') | (df['Title']=='Ms.')])

#   3.2 Products
#      • Color == 'Black' and StandardCost < 50
#      • Size in ['M','L']
#      • Color is not null
df = pd.read_csv(PRODUCT_PATH, sep='|', encoding='latin-1')
df = df[['Color', 'StandardCost', 'Size']]
print(df.loc[ (df['Color']=='Black') & (df['StandardCost']<50)] )
print(df[df['Size'].isin(['M','L'])])
print(df[~df['Color'].isnull() & ~df['Color'].isna()])

#   3.3 OrderHeader
#      • Orders in calendar year 2020
#      • TotalDue between 100 and 1000
#      • ShipDate is null (orders not yet shipped)
df = pd.read_csv(ORDERHEADER_PATH, sep='|', encoding='latin-1')
df = df[['OrderDate', 'TotalDue', 'ShipDate']]
print(df[df['OrderDate'].str[:4]=='2020'])
print(df[(df['TotalDue'] >=100) & (df['TotalDue'] <=1000) ])
print(df[df['ShipDate'].isnull()])

#   3.4 OrderDetails
#      • OrderQty >= 5 or UnitPriceDiscount >= 0.1
#      • LineTotal == OrderQty * UnitPrice (no discount)
#      • UnitPriceDiscount between 0.05 and 0.2
df = pd.read_csv(ORDERDETAILS_PATH, sep='|', encoding='latin-1')
print(df.columns)
df = df[['OrderQty', 'LineTotal', 'UnitPriceDiscount', 'UnitPrice']]
print(df[(df['OrderQty'] >= 5) | (df['UnitPriceDiscount']>=0.1)])
print(df[df['LineTotal'] == df['OrderQty'] * df['UnitPrice']])
print(df[(df['UnitPriceDiscount'] > 0.05) & (df['UnitPriceDiscount']< 0.2) ])

