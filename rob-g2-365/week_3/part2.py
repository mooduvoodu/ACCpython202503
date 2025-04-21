from file_paths import *
import pandas as pd

# Part 2: Row & Column Subsetting
#   2.1 Customers
#      • Select columns CustomerID, FirstName, LastName, EmailAddress, Phone
#      • Use .iloc to pull rows 10–20 inclusive
#      • Use .loc to get CustomerID in [1,5,10] and show FirstName, LastName
#      • Randomly sample 5 customer rows with df.sample(n=5)
df = pd.read_csv(CUSTOMER_PATH, sep='|', encoding='latin-1')
print(df.head())
subdf = df[['CustomerID', 'FirstName', 'LastName', 'EmailAddress', 'Phone']]
print(subdf.head())
print(subdf.iloc[10:20])
print(subdf.loc[[1,5, 10], ['FirstName', 'LastName']])
print(subdf.sample(n=5))

#   2.2 Products
#      • Select ProductID, Name, ListPrice
#      • Filter for ListPrice > 1000, then show Name & ListPrice
#      • Take a random 5% sample: df.sample(frac=0.05)
#      • Use .nsmallest to find the 3 cheapest products by ListPrice
df = pd.read_csv(PRODUCT_PATH, sep='|', encoding='latin-1')
print(df.head())
subdf = df[['ProductID', 'Name', 'ListPrice']]
print(subdf.head())
print(subdf.loc[df['ListPrice']>1000])
print(subdf.sample(frac=0.05))
print(subdf.nsmallest(3,'ListPrice'))

#   2.3 OrderHeader
#      • Select SalesOrderID, OrderDate, Status, TotalDue
#      • Filter where Status == 5 and TotalDue > 500
#      • Use .nlargest to find top 10 orders by TotalDue
df = pd.read_csv(ORDERHEADER_PATH, sep='|', encoding='latin-1')
subdf = df[['SalesOrderID', 'OrderDate', 'Status', 'TotalDue']]
print(subdf.head())
print(subdf.loc[(df['Status']==5) & (df['TotalDue']> 500)])
print(subdf.nlargest(10, 'TotalDue'))

#   2.4 OrderDetails
#      • Select SalesOrderDetailID, OrderQty, UnitPrice, UnitPriceDiscount
#      • Filter rows where UnitPriceDiscount > 0
#      • Use .nsmallest to find the 5 smallest LineTotal rows
df = pd.read_csv(ORDERDETAILS_PATH, sep='|', encoding='latin-1')
subdf = df[['SalesOrderDetailID', 'OrderQty', 'UnitPrice', 'UnitPriceDiscount']]
print(subdf.loc[subdf['UnitPriceDiscount']> 0])
df_smallest = df.nsmallest(5,'LineTotal')
print(df_smallest[['SalesOrderDetailID', 'OrderQty', 'UnitPrice', 'UnitPriceDiscount']])

