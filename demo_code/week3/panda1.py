import pandas as pd

# =============================================================================
# 1. Load the dataset from the provided pipe-delimited CSV file
# =============================================================================
data_url = '/workspaces/ACCpython202503/datasets/orderdetails.csv'
df = pd.read_csv(data_url, delimiter='|')

# Check column names to confirm
print("Column Names:", df.columns.tolist())

# =============================================================================
# 2. Data Exploration Basics
# =============================================================================

print("\n--- Data Exploration ---")

# Shape (rows, columns)
print("\nShape:", df.shape)

# Data types
print("\nData types:")
print(df.dtypes)

# Info summary
print("\nInfo summary:")
df.info()

# First few rows
print("\nHead of DataFrame:")
print(df.head())

# Last few rows
print("\nTail of DataFrame:")
print(df.tail())

# =============================================================================
# 3. Column Selection
# =============================================================================

print("\n--- Column Selection ---")

# Single Column (Series)
sales_order_series = df['SalesOrderID']
print("\nSingle column ('SalesOrderID') as Series:")
print(sales_order_series.head())

# Single Column with dot notation (works if no spaces/special chars)
unit_price_series = df.UnitPrice
print("\nSingle column ('UnitPrice') using dot notation:")
print(unit_price_series.head())

# Multiple Columns selection (DataFrame)
multi_col_df = df[['SalesOrderID', 'ProductID', 'UnitPrice', 'OrderQty']]
print("\nMultiple columns selected ('SalesOrderID', 'ProductID', 'UnitPrice', 'OrderQty'):")
print(multi_col_df.head())

# =============================================================================
# 4. Subsetting Rows using .loc[] and .iloc[]
# =============================================================================

print("\n--- Row Subsetting ---")

# .loc[] example (rows with UnitPrice > 20)
loc_subset = df.loc[df['UnitPrice'] > 20, ['SalesOrderID', 'UnitPrice', 'OrderQty']]
print("\n.loc subset (UnitPrice > 20):")
print(loc_subset.head())

# .loc specific row indices (labels)
loc_specific = df.loc[[0, 2, 4], ['SalesOrderDetailID', 'LineTotal']]
print("\n.loc subset specific rows [0,2,4]:")
print(loc_specific)

# .iloc[] example (integer positions)
iloc_subset = df.iloc[0:5, 0:4]
print("\n.iloc subset (first 5 rows, first 4 columns):")
print(iloc_subset)

# .iloc specific rows and columns
iloc_specific = df.iloc[[0, 1, 3], [1, 4, 6]]
print("\n.iloc subset (rows 0,1,3 and columns 1,4,6):")
print(iloc_specific)

# =============================================================================
# 5. Boolean (Conditional) Row Selection
# =============================================================================

print("\n--- Boolean Row Selection ---")

# Single condition (OrderQty > 10)
qty_over_10 = df[df['OrderQty'] > 10]
print("\nRows with OrderQty > 10:")
print(qty_over_10.head())

# Multiple conditions with AND (&)
high_price_and_qty = df[(df['UnitPrice'] > 20) & (df['OrderQty'] > 5)]
print("\nRows with UnitPrice > 20 AND OrderQty > 5:")
print(high_price_and_qty.head())

# Multiple conditions with OR (|)
high_discount_or_high_qty = df[(df['UnitPriceDiscount'] > 0.2) | (df['OrderQty'] >= 10)]
print("\nRows with UnitPriceDiscount > 0.2 OR OrderQty >= 10:")
print(high_discount_or_high_qty.head())

# =============================================================================
# 6. Explanation of Series vs DataFrame, .loc vs .iloc
# =============================================================================

print("\n--- Explanations ---")

# Series vs DataFrame
print("\n'SalesOrderID' column is a Series:", type(df['SalesOrderID']))
print("'SalesOrderID' and 'ProductID' columns together form a DataFrame:", 
      type(df[['SalesOrderID', 'ProductID']]))

# .loc vs .iloc explanations
print("\n.loc[] uses labels (row index labels and column names).")
print(".iloc[] uses integer positions (numeric indices).")

# Examples
print("\nExample .loc[] (rows 0-2 inclusive, specific columns):")
print(df.loc[0:2, ['SalesOrderID', 'ProductID', 'OrderQty']])

print("\nExample .iloc[] (rows 0-2 inclusive, columns 0-2):")
print(df.iloc[0:3, 0:3])