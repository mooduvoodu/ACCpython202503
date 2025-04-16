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



# =============================================================================
# Explicit, step-by-step GroupBy examples
# =============================================================================

print("\n--- Step-by-Step GroupBy Operations ---")

# Example 1: Grouping by one column and calculating the average UnitPrice

# Step 1: Create groupby object
group_by_product = df.groupby('ProductID')

# Step 2: Select a column to aggregate
unit_price = group_by_product['UnitPrice']

# Step 3: Perform the aggregation (mean)
avg_price_per_product = unit_price.mean()

# Step 4: Reset index to convert Series back to DataFrame
avg_price_per_product_df = avg_price_per_product.reset_index()

print("\nAverage UnitPrice per ProductID (step-by-step):\n", avg_price_per_product_df.head())

# -----------------------------------------------------------------------------

# Example 2: Multiple aggregations with separated steps (mean, max, min, sum)

# Step 1: Create the groupby object
group_by_product = df.groupby('ProductID')

# Step 2: Aggregate UnitPrice with multiple operations
unitprice_agg = group_by_product['UnitPrice'].agg(['mean', 'max', 'min'])

# Step 3: Aggregate OrderQty separately (sum)
orderqty_sum = group_by_product['OrderQty'].sum()

# Step 4: Aggregate LineTotal separately (sum)
linetotal_sum = group_by_product['LineTotal'].sum()

# Step 5: Combine aggregated results into a single DataFrame
aggregated_results = unitprice_agg.join(orderqty_sum).join(linetotal_sum).reset_index()

# Rename columns for clarity
aggregated_results.columns = ['ProductID', 'Avg_UnitPrice', 'Max_UnitPrice', 'Min_UnitPrice', 'Total_OrderQty', 'Total_LineTotal']

print("\nMultiple aggregations combined into single DataFrame (step-by-step):\n", aggregated_results.head())

# -----------------------------------------------------------------------------

# Example 3: Grouping by multiple columns step-by-step

# Step 1: Define the grouping
group_by_product_orderqty = df.groupby(['ProductID', 'OrderQty'])

# Step 2: Aggregate LineTotal
linetotal_by_product_orderqty = group_by_product_orderqty['LineTotal'].sum()

# Step 3: Reset index
linetotal_by_product_orderqty_df = linetotal_by_product_orderqty.reset_index()

print("\nLineTotal by ProductID and OrderQty (step-by-step):\n", linetotal_by_product_orderqty_df.head())

# -----------------------------------------------------------------------------

# Example 4: Filtering grouped data (separated clearly)

# Step 1: Perform initial grouping
grouped_linetotal = df.groupby('ProductID')['LineTotal'].sum()

# Step 2: Filter groups (products) with total LineTotal > 1000
high_value_products = grouped_linetotal[grouped_linetotal > 1000]

# Step 3: Reset index for better readability
high_value_products_df = high_value_products.reset_index()

print("\nFiltered grouped data (Products with total LineTotal > 1000, step-by-step):\n", high_value_products_df.head())

# -----------------------------------------------------------------------------

# Example 5: Sorting Grouped Results explicitly step-by-step

# Step 1: Group and aggregate (total sales by product)
total_sales_by_product = df.groupby('ProductID')['LineTotal'].sum()

# Step 2: Sort aggregated results in descending order
sorted_sales_by_product = total_sales_by_product.sort_values(ascending=False)

# Step 3: Select top 5 products
top_5_products = sorted_sales_by_product.head(5)

# Step 4: Reset index
top_5_products_df = top_5_products.reset_index()

# Rename columns
top_5_products_df.columns = ['ProductID', 'TotalSales']

print("\nTop 5 products by total LineTotal (step-by-step):\n", top_5_products_df)


# =============================================================================
# Multi-column GroupBy clearly demonstrated with reset_index()
# =============================================================================

print("\n--- GroupBy Multiple Columns and Flatten with reset_index() ---")

# Step 1: Perform Multi-column GroupBy
grouped = df.groupby(['ProductID', 'OrderQty'])['LineTotal'].sum()

print("\nGrouped data BEFORE reset_index (Multi-index):")
print(grouped.head())

# Step 2: Flatten the multi-index result using reset_index()
grouped_flattened = grouped.reset_index()

print("\nGrouped data AFTER reset_index (Flattened DataFrame):")
print(grouped_flattened.head())

# Verify the types before and after
print("\nType before reset_index:", type(grouped))
print("Type after reset_index:", type(grouped_flattened))



# =============================================================================
# GroupBy operations with nunique() method
# =============================================================================

print("\n--- GroupBy with nunique() ---")

# Example 1: Count unique ProductIDs per SalesOrderID

unique_products_per_order = df.groupby('SalesOrderID')['ProductID'].nunique().reset_index()
unique_products_per_order.columns = ['SalesOrderID', 'UniqueProductCount']

print("\nNumber of unique ProductIDs per SalesOrderID:\n", unique_products_per_order.head())

# Example 2: Count unique SalesOrderIDs per ProductID

unique_orders_per_product = df.groupby('ProductID')['SalesOrderID'].nunique().reset_index()
unique_orders_per_product.columns = ['ProductID', 'UniqueOrderCount']

print("\nNumber of unique SalesOrderIDs per ProductID:\n", unique_orders_per_product.head())

# =============================================================================
# GroupBy operations with value_counts() method
# =============================================================================

print("\n--- GroupBy with value_counts() ---")

# Example 1: Frequency of OrderQty values for each ProductID

orderqty_counts_per_product = df.groupby('ProductID')['OrderQty'].value_counts().reset_index(name='Count')
orderqty_counts_per_product.columns = ['ProductID', 'OrderQty', 'Frequency']

print("\nFrequency of OrderQty per ProductID:\n", orderqty_counts_per_product.head(10))

# Example 2: Frequency of UnitPriceDiscount values for each ProductID

discount_counts_per_product = df.groupby('ProductID')['UnitPriceDiscount'].value_counts().reset_index(name='Count')
discount_counts_per_product.columns = ['ProductID', 'UnitPriceDiscount', 'Frequency']

print("\nFrequency of UnitPriceDiscount per ProductID:\n", discount_counts_per_product.head(10))



# =============================================================================
# Demonstrating Automatic Alignment and Vectorized Operations (Broadcasting)
# =============================================================================

print("\n--- Automatic Alignment and Vectorization Examples ---")

# Example 1: Simple arithmetic operations between Series
# Compute actual discounted price per unit: UnitPrice - (UnitPrice * UnitPriceDiscount)

df['DiscountedPrice'] = df['UnitPrice'] - (df['UnitPrice'] * df['UnitPriceDiscount'])
print("\nDiscounted Price calculation (vectorized operation):")
print(df[['UnitPrice', 'UnitPriceDiscount', 'DiscountedPrice']].head())

# ----------------------------------------------------------------------------

# Example 2: Multiply two aligned Series to compute LineTotal (OrderQty * DiscountedPrice)

df['ComputedLineTotal'] = df['OrderQty'] * df['DiscountedPrice']
print("\nComputed LineTotal (OrderQty * DiscountedPrice):")
print(df[['OrderQty', 'DiscountedPrice', 'ComputedLineTotal']].head())

# ----------------------------------------------------------------------------

# Example 3: Demonstrate automatic alignment based on index
# Let's create two Series with shuffled indices and demonstrate automatic alignment clearly

# Shuffle df to create misaligned indices
shuffled_df = df.sample(frac=1).reset_index(drop=True)

# Original Series with proper alignment
original_series = df['UnitPrice']

# Shuffled Series
shuffled_series = shuffled_df['UnitPrice']

# Perform addition (automatically aligned based on index)
aligned_sum = original_series + shuffled_series

print("\nAligned sum of original and shuffled Series (automatic alignment):")
print("Original Series head:\n", original_series.head())
print("Shuffled Series head:\n", shuffled_series.head())
print("Aligned sum head (Notice NaNs due to misaligned indices):\n", aligned_sum.head(10))

# ----------------------------------------------------------------------------

# Example 4: Handling alignment explicitly (when indices differ)

# To correctly align data explicitly by resetting indices
aligned_sum_fixed = original_series.reset_index(drop=True) + shuffled_series.reset_index(drop=True)

print("\nExplicitly aligned sum (after resetting indices):")
print(aligned_sum_fixed.head(10))

# ----------------------------------------------------------------------------

# Example 5: Broadcasting operation with a scalar (applied to entire Series)

# Increase UnitPrice by a fixed scalar (e.g., 10%)
df['IncreasedUnitPrice'] = df['UnitPrice'] * 1.10

print("\nUnitPrice increased by 10% (scalar broadcasting):")
print(df[['UnitPrice', 'IncreasedUnitPrice']].head())