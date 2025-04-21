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
