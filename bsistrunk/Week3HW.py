# Lab: Pandas Operations on Pipe‑Delimited CSV Files
#
# You have four pipe‑delimited files:
#    /workspaces/ACCpython202503/datasets/customers.csv
#    /workspaces/ACCpython202503/datasets/product.csv
#    /workspaces/ACCpython202503/datasets/orderheader.csv
#    /workspaces/ACCpython202503/datasets/orderdetails.csv
#
# In this expanded lab you will:
#  1. Import each CSV into pandas DataFrames
#  2. Profile the data: shapes, dtypes, summary statistics
#  3. Practice row & column subsetting (multiple methods)
#  4. Practice row filtering with boolean logic (including negation & multiple criteria)
#  5. Run groupby aggregates (single & multi‑column, nunique, transform)
#  6. Do simple profiling: .shape, .nunique(), .value_counts(), percent distributions, cumulative sums
#
# No merges or joins—each DataFrame is used in isolation.
#
# Part 1: Import & Profile
#   - Read each file from path property
#       df = pd.read_csv('path/to/file.csv', sep='|', encoding='latin-1')
#   - For each DataFrame inspect:
#       df.shape
#       df.columns
#       df.dtypes
#       df.head()
#       df.info()
#       df.describe()
#
# Part 2: Row & Column Subsetting
#   2.1 Customers
#      • Select columns CustomerID, FirstName, LastName, EmailAddress, Phone
#      • Use .iloc to pull rows 10–20 inclusive
#      • Use .loc to get CustomerID in [1,5,10] and show FirstName, LastName
#      • Randomly sample 5 customer rows with df.sample(n=5)
#
#   2.2 Products
#      • Select ProductID, Name, ListPrice
#      • Filter for ListPrice > 1000, then show Name & ListPrice
#      • Take a random 5% sample: df.sample(frac=0.05)
#      • Use .nsmallest to find the 3 cheapest products by ListPrice
#
#   2.3 OrderHeader
#      • Select SalesOrderID, OrderDate, Status, TotalDue
#      • Filter where Status == 5 and TotalDue > 500
#      • Use .nlargest to find top 10 orders by TotalDue
#
#   2.4 OrderDetails
#      • Select SalesOrderDetailID, OrderQty, UnitPrice, UnitPriceDiscount
#      • Filter rows where UnitPriceDiscount > 0
#      • Use .nsmallest to find the 5 smallest LineTotal rows
#
# Part 3: Boolean Row Filtering
#   3.1 Customers
#      • FirstName startswith A or J
#      • MiddleName is not null
#      • FirstName contains 'ar' (case‑insensitive)
#      • Title not in ['Mr.','Ms.']
#
#   3.2 Products
#      • Color == 'Black' and StandardCost < 50
#      • Size in ['M','L']
#      • Color is not null
#
#   3.3 OrderHeader
#      • Orders in calendar year 2020
#      • TotalDue between 100 and 1000
#      • ShipDate is null (orders not yet shipped)
#
#   3.4 OrderDetails
#      • OrderQty >= 5 or UnitPriceDiscount >= 0.1
#      • LineTotal == OrderQty * UnitPrice (no discount)
#      • UnitPriceDiscount between 0.05 and 0.2
#
# Part 4: GroupBy & Aggregates
#   4.1 Customers
#      • Count of customers per SalesPerson
#      • Title distribution via .value_counts()
#      • Group by SalesPerson & Title, count customers
#
#   4.2 Products
#      • Group by Color: mean, min, max of ListPrice
#      • Group by Size: count products
#      • Group by Color & Size: average ListPrice and count
#      • Count of unique ProductNumber per Color
#
#   4.3 OrderHeader
#      • Group by order_date (date only) to sum TotalDue
#      • Group by Status: count & mean TotalDue
#      • Group by calendar month: count orders & sum TotalDue
#      • Use .transform('sum') to compute each order’s percentage of daily sales
#
#   4.4 OrderDetails
#      • Group by ProductID: sum OrderQty, mean UnitPriceDiscount
#      • OrderQty distribution via .value_counts()
#      • Group by ProductID & OrderQty: count rows
#      • Compute cumulative sum of OrderQty over sorted SalesOrderID
#
# Part 5: Simple Profiling
#   • Total rows per DataFrame
#   • Unique EmailAddress count in customers
#   • Rows with discount > 0 in order details
#   • value_counts of UnitPriceDiscount
#   • value_counts & percent of Status in order header
#   • Percent distribution of SalesPerson in customers
#   • Count of discontinued products (DiscontinuedDate not null)
#   • Average LineTotal in order details


import pandas as pd

customers = pd.read_csv('/workspaces/ACCpython202503/datasets/customers.csv', sep='|', encoding='latin-1')
product = pd.read_csv('/workspaces/ACCpython202503/datasets/product.csv', sep='|', encoding='latin-1')
order_header = pd.read_csv('/workspaces/ACCpython202503/datasets/orderheader.csv', sep='|', encoding='latin-1')
order_details = pd.read_csv('/workspaces/ACCpython202503/datasets/orderdetails.csv', sep='|', encoding='latin-1')

#Parse Dates
for col in ['OrderDate','DueDate','ShipDate']:
    order_header[col] = pd.to_datetime(order_header[col], errors='coerce')

#Part 1: Profile
for name, df in [
    ('Customers', customers),
    ('Products', product),
    ('OrderHeader', order_header),
    ('OrderDetails', order_details),]:

    print(f"\n=== {name} ===")
    print("Shape:", df.shape)
    print("Columns:", df.columns)
    print("DTypes:", df.dtypes)
    print(df.head)
    print(df.info)
    print(df.describe)


# Part 2: Subsetting
# 2.1 Customers
# Select columns CustomerID, FirstName, LastName, EmailAddress, Phone
cust_sel = customers[['CustomerID', 'FirstName', 'LastName', 'EmailAddress', 'Phone']]

# Use .iloc to pull rows 10–20 inclusive
cust_10_20 = cust_sel.iloc[9:20]

# Use .loc to get CustomerID in [1,5,10] and show FirstName, LastName
cust_loc = customers.loc[customers['CustomerID'].isin([1,5,10]),['FirstName','LastName']]

# Randomly sample 5 customer rows with df.sample(n=5)
cust_sample = customers.sample(n = 5, random_state = 1)

#2.2 Products
# Select ProductID, Name, ListPrice
prod_sel = product[['ProductID','Name','ListPrice']]

# Filter for ListPrice > 1000, then show Name & ListPrice
prod_filter = prod_sel[prod_sel['ListPrice']>1000]

# Take a random 5% sample: df.sample(frac=0.05)
prod_sample = prod_sel.sample(frac=0.05, random_state=1)

# Use .nsmallest to find the 3 cheapest products by ListPrice
prod_cheap = prod_sel.nsmallest(3, 'ListPrice')

#2.3 Order Header
# Select SalesOrderID, OrderDate, Status, TotalDue
oh_sel = order_header[['SalesOrderID','OrderDate','Status','TotalDue']]

# Filter where Status == 5 and TotalDue > 500
oh_filter = oh_sel[(oh_sel['Status'] == 5) & (oh_sel['TotalDue'] > 500)]

# Use .nlargest to find top 10 orders by TotalDue
oh_large = oh_sel.nlargest(10, 'TotalDue')

#2.4 Order Details
# Select SalesOrderDetailID, OrderQty, UnitPrice, UnitPriceDiscount
od_sel = order_details[['SalesOrderDetailID','OrderQty','UnitPrice','UnitPriceDiscount','LineTotal']]

# Filter rows where UnitPriceDiscount > 0
od_filter = od_sel[od_sel['UnitPriceDiscount'] > 0]

# Use .nsmallest to find the 5 smallest LineTotal rows
od_small = od_sel.nsmallest(5, 'LineTotal')


# Part 3: Boolean Filtering
# 3.1 Customers
# FirstName starts with A or J
cust_AJ = customers[customers['FirstName'].str.startswith(('A','J'), na = False)]

# MiddleName is not null
cust_middle = customers[customers['MiddleName'].notna()]

# FirstName contains 'ar' (case‑insensitive)
cust_contains = customers[customers['FirstName'].str.contains('ar', case = False, na = False)]

# Title not in ['Mr.','Ms.']
cust_titles = customers[customers['Title'].isin(['Mr.','Ms.'])]

# 3.2 Products
# Color == 'Black' and StandardCost < 50
prod_color = product[(product['Color'] == 'Black') & (product['StandardCost'] < 50)]

# Size in ['M','L']
prod_size = product[product['Size'].isin(['M','L'])]

# Color is not null
prod_not_null = product[product['Color'].notna()] #Why notna instead of notnull?

# 3.2 Order Header
# Orders in calendar year 2020
oh_2020 = order_header[(order_header['OrderDate'].dt.year == 2020)]

# TotalDue between 100 and 1000
oh_total_due = order_header[order_header['TotalDue'].between(100,1000)]

# ShipDate is null (orders not yet shipped)
oh_shipped = order_header[order_header['ShipDate'].isna()]

# 3.2 Order Details
# OrderQty >= 5 or UnitPriceDiscount >= 0.1
od_large = order_details[(order_details['OrderQty'] >= 5) | (order_details['UnitPriceDiscount'] >= 0.1)]

# LineTotal == OrderQty * UnitPrice (no discount)
od_no_disc = order_details[order_details['LineTotal'] == order_details['OrderQty'] * order_details['UnitPrice']]

# UnitPriceDiscount between 0.05 and 0.2
od_disc_range = order_details[order_details['UnitPriceDiscount'].between(.05,.2)]

# Part 4: GroupBy & Aggregates
# 4.1 Customers
# Count of customers per SalesPerson
cust_by_sp = customers.groupby('SalesPerson').size()

# Title distribution via .value_counts()
title_counts = customers['Title'].value_counts()

# Group by SalesPerson & Title, count customers
cust_sp_title = customers.groupby(['SalesPerson','Title']).size()

# 4.2 Products
# Group by Color: mean, min, max of ListPrice
price_stats = product.groupby('Color')['ListPrice'].agg(['mean','min','max'])

# Group by Size: count products
size_counts = product.groupby('Size').size()

# Group by Color & Size: average ListPrice and count
color_size_stats = product.groupby(['Color','Size'])['ListPrice'].agg(['mean','count'])

# Count of unique ProductNumber per Color
unique_models = product.groupby('Color')['ProductNumber'].nunique

# 4.3 Order Header
# Group by order_date (date only) to sum TotalDue
daily_sales = order_header.groupby(order_header['OrderDate'].dt.date)['TotalDue'].sum()

# Group by Status: count & mean TotalDue
status_stats = order_header.groupby('Status')['TotalDue'].agg(['mean','count'])

# Group by calendar month: count orders & sum TotalDue
monthly_stats = order_header.groupby(order_header['OrderDate'].dt.to_period('M')).agg(
    Orders=('SalesOrderID','count'),
    Sales=('TotalDue','sum'))

# Use .transform('sum') to compute each order’s percentage of daily sales
order_header['DailyPct'] = order_header['TotalDue'] / order_header.groupby(order_header['OrderDate'].dt.date)['TotalDue'].transform('sum')

# 4.4 Order Details
# Group by ProductID: sum OrderQty, mean UnitPriceDiscount
prod_qty_disc = order_details.groupby('ProductID').agg(
    TotalQty=('OrderQty','sum'),
    AvgDisc=('UnitPriceDiscount','mean'))

# OrderQty distribution via .value_counts()
orderqty_dist = order_details['OrderQty'].value_counts()

# Group by ProductID & OrderQty: count rows
prod_qty_count = order_details.groupby(['ProductID','OrderQty']).size()

# Compute cumulative sum of OrderQty over sorted SalesOrderID
orders_d = order_details.sort_values('SalesOrderID')
orders_d['CumQty'] = order_details['OrderQty'].cumsum()

# Part 5: Simple Profiling
print("Customers rows:", customers.shape[0])
print("Unique emails:", customers['EmailAddress'].nunique())
print("SalesPerson % distribution:\n", customers['SalesPerson'].value_counts(normalize=True))
print("Discontinued products:", product['DiscontinuedDate'].notna().sum())
print("OrderDetails rows:", order_details.shape[0])
print("Rows w/ discount >0:", (order_details['UnitPriceDiscount']>0).sum())
print("Discount value counts:\n", order_details['UnitPriceDiscount'].value_counts())
print("Avg LineTotal:", order_details['LineTotal'].mean())
print("OrderHeader Status counts & %:\n", order_header['Status'].value_counts(dropna=False))
print("OrderHeader Status %:\n", order_header['Status'].value_counts(normalize=True))