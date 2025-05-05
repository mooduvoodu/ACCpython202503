# ================== Student Exercises ==================
# Using the pipe-delimited CSVs (customers.csv, orderheader.csv, orderdetails.csv, product.csv):
# 1. Read each file into a DataFrame with pd.read_csv(sep='|', encoding='latin1').
# 2. Drop any rows where the key ID columns are null:
#      - customers: CustomerID
#      - orderheader: SalesOrderID & CustomerID
#      - orderdetails: SalesOrderID & ProductID
#      - product: ProductID
# 3. Vertically concatenate (axis=0) the first 3 and last 3 rows of orderheader,
#    resetting the index.
# 4. Horizontally concatenate (axis=1) customer names and order totals for three
#    common CustomerID values—align on CustomerID.
# 5. Concatenate rows with different columns: stack first 2 rows of customers
#    (CustomerID, FirstName) with first 2 rows of product (ProductID, Name).
# 6. Concatenate columns with different row counts: side-by-side concat of the
#    two DataFrames from (5).
# 7. Perform an inner join of orderheader ↔ orderdetails on SalesOrderID.
# 8. Perform a left join of orderdetails → product on ProductID.
# 9. Perform a right join of orderdetails → product on ProductID.
# 10. Perform a full outer join of customers ↔ orderheader on CustomerID.
# 11. Perform a cross join of customers × product.
# 12. Use apply() to compute a new column 'LineTotal' in orderdetails
#     by multiplying UnitPrice × OrderQty.
# 13. Use apply() to produce 'Subtotal', 'Tax', and 'TotalWithTax' for each
#     orderdetails row (via a function returning a Series), then use concat()
#     to merge these new columns back into the original orderdetails.

from file_paths import *

# 1. Read each file into a DataFrame with pd.read_csv(sep='|', encoding='latin1').
df_customers = read_customers()
df_orderheaders = read_order_headers()
df_orderdetails = read_order_details()
df_products = read_products()

# 2. Drop any rows where the key ID columns are null:
#      - customers: CustomerID
#      - orderheader: SalesOrderID & CustomerID
#      - orderdetails: SalesOrderID & ProductID
#      - product: ProductID
#df_customers1 = df_customers.dropna(subset=['CustomerID'])
#df_orderheaders1 = df_orderheaders.dropna(subset=['SalesOrderID', 'CustomerID'])
#df_orderdetails1 = df_orderdetails.dropna(subset=['SalesOrderID', 'ProductID'])
#df_products1 = df_products.dropna(subset=['ProductID'])

# 3. Vertically concatenate (axis=0) the first 3 and last 3 rows of orderheader,
#    resetting the index.
# df_head = df_orderheaders.head(3)
# df_tail = df_orderheaders.tail(3)
# df_headers2 = pd.concat([df_head, df_tail], ignore_index=True)

# 4. Horizontally concatenate (axis=1) customer names and order totals for three
#    common CustomerID values—align on CustomerID.
# Solution 4: Horizontal concat customers ↔ order totals for 3 CustomerIDs
#common_ids = sorted(set(df_customers['CustomerID']) & set(df_orderheaders['CustomerID']))
#sample_ids = common_ids[:3]
#df_customers3 = df_customers.set_index('CustomerID')
#df_customers4 = df_customers3[['FirstName','LastName']]
#df_customers5 = df_customers4.loc[sample_ids]

#cust_sub   = (df_customers
#              .set_index('CustomerID')[['FirstName','LastName']]
#              .loc[sample_ids])
#oh_sub     = (df_orderheaders
#              .set_index('CustomerID')[['SalesOrderNumber','TotalDue']]
#              .loc[sample_ids])
# concat_horz = pd.concat([cust_sub, oh_sub], axis=1)


# 5. Concatenate rows with different columns: stack first 2 rows of customers
#    (CustomerID, FirstName) with first 2 rows of product (ProductID, Name).
# Solution 5: Concat rows with different columns
#df_small_cust = df_customers[['CustomerID','FirstName']].head(2)
#df_small_prod = df_products[['ProductID','Name']].head(2)
#concat_diff_cols = pd.concat([df_small_cust, df_small_prod], axis=0, sort=False)

# 6. Concatenate columns with different row counts: side-by-side concat of the
#    two DataFrames from (5).
#concat_diff_rows = pd.concat([df_small_cust, df_small_prod], axis=1)

# 7. Perform an inner join of orderheader ↔ orderdetails on SalesOrderID.
#inner_join = pd.merge(df_orderheaders, df_orderdetails, on='SalesOrderID', how='inner')

# 8. Perform a left join of orderdetails → product on ProductID.
#left_join = pd.merge(df_orderdetails, df_products, on='ProductID', how='left')

# 9. Perform a right join of orderdetails → product on ProductID.
#right_join = pd.merge(df_orderdetails, df_products, on='ProductID', how='right')

# 10. Perform a full outer join of customers ↔ orderheader on CustomerID.
#outer_join = pd.merge(df_customers, df_orderheaders, on='CustomerID', how = 'outer')

#df_customers6 = df_customers.copy()
#df_products2 = df_products.copy()
#df_customers6['key'] = 0
#df_products2['key'] = 0
# 11. Perform a cross join of customers × product.
#cross_join = pd.merge(df_customers6, df_products2, on='key').drop('key', axis=1)


# 12. Use apply() to compute a new column 'LineTotal' in orderdetails
#     by multiplying UnitPrice × OrderQty.
#df_orderdetails2 = df_orderdetails.copy()
#df_orderdetails2['LineTotal2'] = df_orderdetails.apply(lambda row: row['UnitPrice'] * row['OrderQty'], axis=1)

# 13. Use apply() to produce 'Subtotal', 'Tax', and 'TotalWithTax' for each
#     orderdetails row (via a function returning a Series), then use concat()
#     to merge these new columns back into the original orderdetails.
series_subtotal = df_orderheaders['SubTotal']
series_tax = df_orderheaders['TaxAmt']
series_total_with_tax = df_orderheaders['TotalDue']

df_orderdetails3 = df_orderdetails.copy()
df_orderdetails4= pd.concat([df_orderdetails3, series_subtotal, series_tax, series_total_with_tax] )
