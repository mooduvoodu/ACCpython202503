from file_paths import *
import pandas as pd

# Part 4: GroupBy & Aggregates
#   4.1 Customers
#      • Count of customers per SalesPerson
#      • Title distribution via .value_counts()
#      • Group by SalesPerson & Title, count customers
df = pd.read_csv(CUSTOMER_PATH, sep='|', encoding='latin-1')
#print(df.groupby('SalesPerson').size())
#print(df.columns)
#print(df['Title'].value_counts())
# print(df.groupby(['SalesPerson', 'Title']).size())

#   4.2 Products
#      • Group by Color: mean, min, max of ListPrice
#      • Group by Size: count products
#      • Group by Color & Size: average ListPrice and count
#      • Count of unique ProductNumber per Color
df = pd.read_csv(PRODUCT_PATH, sep='|', encoding='latin-1')
# print(df.columns)
# print(df.groupby('Color')['ListPrice'].agg(['mean', 'min', 'max'] ))
# print(df.groupby('Size')['ProductID'].size())
# print(df.groupby(['Color','Size'])['ListPrice'].agg(['mean', 'count']))
# print(df.groupby('Color')['ProductNumber'].nunique())

#   4.3 OrderHeader
#      • Group by order_date (date only) to sum TotalDue
#      • Group by Status: count & mean TotalDue
#      • Group by calendar month: count orders & sum TotalDue
#      • Use .transform('sum') to compute each order’s percentage of daily sales
df = pd.read_csv(ORDERHEADER_PATH, sep='|', encoding='latin-1')
# print(df['Status'].to_string())
print(df.columns)
print(df.dtypes)
df['OrderDate'] = pd.to_datetime(df['OrderDate'])
print(df[['OrderDate', 'SalesOrderID', 'TotalDue']])
print(df.dtypes)
# print(df[['OrderDate']].to_string())
# print(df.groupby('OrderDate')['TotalDue'].agg(['sum']))
# print(df.groupby('Status')['TotalDue'].agg(['count', 'mean']))
# print(df['OrderDate'].dt.strftime('%B'))
print(df.groupby(df['OrderDate'].dt.month))

# Why doesn't this work?
# print(df.groupby(df['OrderDate'].dt.month).agg({'SalesOrderID':'count'}, {'TotalDue': 'sum'}))
print(df.groupby(df['OrderDate'].dt.month).agg(Orders = ('SalesOrderID','count'), Sales = ('TotalDue', 'sum')))

#      • Use .transform('sum') to compute each order’s percentage of daily sales

# **** Don't know what you are asking ****