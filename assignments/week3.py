# Lab: Pandas Operations on Pipe‑Delimited CSV Files
#
# You have four pipe‑delimited files:
#     /workspaces/ACCpython202503/datasets/customers.csv
#    /workspaces/ACCpython202503/datasets/product.csv
#   /workspaces/ACCpython202503/datasets/orderheader.csv
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
#















# ----- Solutions -----
import pandas as pd

# Load
customers = pd.read_csv('/workspaces/ACCpython202503/datasets/customers.csv', sep='|', encoding='latin-1')
products  = pd.read_csv('/workspaces/ACCpython202503/datasets/product.csv',   sep='|', encoding='latin-1')
orders_h  = pd.read_csv('/workspaces/ACCpython202503/datasets/orderheader.csv',sep='|', encoding='latin-1')
orders_d  = pd.read_csv('/workspaces/ACCpython202503/datasets/orderdetails.csv',sep='|', encoding='latin-1')

# Parse dates
for col in ['OrderDate','DueDate','ShipDate']:
    orders_h[col] = pd.to_datetime(orders_h[col], errors='coerce')

# Part 1: Profile
for name, df in [
    ('Customers', customers),
    ('Products' , products),
    ('OrderHeader', orders_h),
    ('OrderDetails', orders_d),
]:
    print(f"\n=== {name} ===")
    print("Shape:", df.shape)
    print("Columns:", df.columns.tolist())
    print("Dtypes:\n", df.dtypes)
    print(df.head(2))
    df.info()
    print(df.describe(include='all'))

# Part 2: Subsetting
cust_sel        = customers[['CustomerID','FirstName','LastName','EmailAddress','Phone']]
cust_10_20      = cust_sel.iloc[9:20]
cust_loc        = customers.loc[customers['CustomerID'].isin([1,5,10]), ['FirstName','LastName']]
cust_sample     = customers.sample(n=5, random_state=1)

prod_sel        = products[['ProductID','Name','ListPrice']]
prod_expensive  = prod_sel[prod_sel['ListPrice']>1000]
prod_sample_frac= prod_sel.sample(frac=0.05, random_state=1)
prod_cheapest   = prod_sel.nsmallest(3, 'ListPrice')

oh_sel          = orders_h[['SalesOrderID','OrderDate','Status','TotalDue']]
oh_filtered     = oh_sel[(oh_sel['Status']==5)&(oh_sel['TotalDue']>500)]
oh_top10        = oh_sel.nlargest(10, 'TotalDue')

od_sel          = orders_d[['SalesOrderDetailID','OrderQty','UnitPrice','UnitPriceDiscount','LineTotal']]
od_discount     = od_sel[od_sel['UnitPriceDiscount']>0]
od_smallest     = od_sel.nsmallest(5, 'LineTotal')

# Part 3: Boolean Filtering
cust_AJ         = customers[customers['FirstName'].str.startswith(('A','J'), na=False)]
cust_middle     = customers[customers['MiddleName'].notna()]
cust_contains   = customers[customers['FirstName'].str.contains('ar', case=False, na=False)]
cust_not_titles = customers[~customers['Title'].isin(['Mr.','Ms.'])]

prod_black_cost = products[(products['Color']=='Black') & (products['StandardCost']<50)]
prod_sizeML     = products[products['Size'].isin(['M','L'])]
prod_color_nn   = products[products['Color'].notna()]

oh_2020         = orders_h[(orders_h['OrderDate'].dt.year==2020)]
oh_td_range     = orders_h[orders_h['TotalDue'].between(100,1000)]
oh_ship_null    = orders_h[orders_h['ShipDate'].isna()]

od_large        = orders_d[(orders_d['OrderQty']>=5) | (orders_d['UnitPriceDiscount']>=0.1)]
od_no_disc      = orders_d[orders_d['LineTotal']==orders_d['OrderQty']*orders_d['UnitPrice']]
od_disc_range   = orders_d[orders_d['UnitPriceDiscount'].between(0.05,0.2)]

# Part 4: GroupBy & Aggregates
cust_by_sp      = customers.groupby('SalesPerson').size()
title_counts    = customers['Title'].value_counts()
cust_sp_title   = customers.groupby(['SalesPerson','Title']).size()

price_stats     = products.groupby('Color')['ListPrice'].agg(['mean','min','max'])
size_counts     = products.groupby('Size').size()
color_size_stats= products.groupby(['Color','Size'])['ListPrice'].agg(['mean','count'])
unique_models   = products.groupby('Color')['ProductNumber'].nunique()

daily_sales     = orders_h.groupby(orders_h['OrderDate'].dt.date)['TotalDue'].sum()
status_stats    = orders_h.groupby('Status')['TotalDue'].agg(['count','mean'])
monthly_stats   = orders_h.groupby(orders_h['OrderDate'].dt.to_period('M')).agg(
    Orders=('SalesOrderID','count'),
    Sales=('TotalDue','sum')
)
orders_h['DailyPct'] = orders_h['TotalDue'] / orders_h.groupby(orders_h['OrderDate'].dt.date)['TotalDue'].transform('sum')

prod_qty_disc   = orders_d.groupby('ProductID').agg(
    TotalQty=('OrderQty','sum'),
    AvgDisc=('UnitPriceDiscount','mean')
)
orderqty_dist   = orders_d['OrderQty'].value_counts()
prod_qty_count  = orders_d.groupby(['ProductID','OrderQty']).size()
orders_d = orders_d.sort_values('SalesOrderID')
orders_d['CumQty'] = orders_d['OrderQty'].cumsum()

# Part 5: Simple Profiling
print("Customers rows:", customers.shape[0])
print("Unique emails:", customers['EmailAddress'].nunique())
print("SalesPerson % distribution:\n", customers['SalesPerson'].value_counts(normalize=True))
print("Discontinued products:", products['DiscontinuedDate'].notna().sum())
print("OrderDetails rows:", orders_d.shape[0])
print("Rows w/ discount >0:", (orders_d['UnitPriceDiscount']>0).sum())
print("Discount value counts:\n", orders_d['UnitPriceDiscount'].value_counts())
print("Avg LineTotal:", orders_d['LineTotal'].mean())
print("OrderHeader Status counts & %:\n", orders_h['Status'].value_counts(dropna=False))
print("OrderHeader Status %:\n", orders_h['Status'].value_counts(normalize=True))
