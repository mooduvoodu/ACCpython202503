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

import pandas as pd

# 1. Read each file into a DataFrame with pd.read_csv(sep='|', encoding='latin1')
customers = pd.read_csv('/workspaces/ACCpython202503/datasets/customers.csv', sep='|', encoding='latin1')
order_header = pd.read_csv('/workspaces/ACCpython202503/datasets/orderheader.csv', sep='|', encoding='latin1')
order_details = pd.read_csv('/workspaces/ACCpython202503/datasets/orderdetails.csv', sep='|', encoding='latin1')
product = pd.read_csv('/workspaces/ACCpython202503/datasets/product.csv', sep='|', encoding='latin1')

# 2. Drop any rows where the key ID columns are null:
#      - customers: CustomerID
#      - orderheader: SalesOrderID & CustomerID
#      - orderdetails: SalesOrderID & ProductID
#      - product: ProductID
customers = customers.dropna(subset = ['CustomerID'])
orderheader = order_header.dropna(subset = ['SalesOrderID','CustomerID'])
orderdetails = order_details.dropna(subset = ['SalesOrderID','ProductID'])
product = product.dropna(subset = ['ProductID'])

# 3. Vertically concatenate (axis=0) the first 3 and last 3 rows of orderheader, resetting the index
ohtop3 = order_header.head(3)
ohbot3 = order_header.tail(3)
concat_vert = pd.concat([ohtop3,ohbot3], axis = 0, ignore_index = True)

# 4. Horizontally concatenate (axis=1) customer names and order totals for three common CustomerID values — align on CustomerID.
common_ids = sorted(set(customers['CustomerID']) & set(orderheader['CustomerID']))
sample_ids = common_ids[:3]
cust_sub = (customers
            .set_index('CustomerID')[['FirstName','LastName']]
            .loc[sample_ids])
oh_sub = (orderheader
             .set_index('CustomerID')[['SalesOrderNumber','TotalDue']]
             .loc[sample_ids])
concat_horz = pd.concat([cust_sub,oh_sub], axis = 1)

# 5. Concatenate rows with different columns: stack first 2 rows of customers (CustomerID, FirstName) with first 2 rows of product (ProductID, Name).
df_small_cust = customers[['CustomerID','FirstName']].head(2)
df_small_prod = product[['ProductID','Name']].head(2)
concat_diff_cols = pd.concat([df_small_cust, df_small_prod], axis = 0, sort = False)

# 6. Concatenate columns with different row counts: side-by-side concat of the two DataFrames from (5).
concat_diff_rows = pd.concat([df_small_cust,df_small_prod], axis = 1)

# 7. Perform an inner join of orderheader ↔ orderdetails on SalesOrderID.
inner = pd.merge(
    orderheader,
    orderdetails[['SalesOrderID','OrderQty','UnitPrice']],
    on = 'SalesOrderID',
    how = 'inner')

# 8. Perform a left join of orderdetails → product on ProductID.
left = pd.merge(
    orderdetails,
    product[['ProductID','Name','ListPrice']],
    on = 'ProductID',
    how = 'left')

# 9. Perform a right join of orderdetails → product on ProductID.
right = pd.merge(
    orderdetails,
    product[['ProductID','Name']],
    on = 'ProductID',
    how = 'right')

# 10. Perform a full outer join of customers ↔ orderheader on CustomerID.
outer = pd.merge(
    customers[['CustomerID','FirstName','LastName']],
    orderheader[['CustomerID','SalesOrderNumber','TotalDue']],
    on = 'CustomerID',
    how = 'outer')

# 11. Perform a cross join of customers × product.
cross = pd.merge(
    customers[['CustomerID']],
    product[['ProductID']],
    how = 'cross')

# 12. Use apply() to compute a new column 'LineTotal' in orderdetails by multiplying UnitPrice × OrderQty.
orderdetails['LineTotal'] = orderdetails.apply(
    lambda row: row['UnitPrice'] * row['OrderQty'],
    axis = 1)

# 13. Use apply() to produce 'Subtotal', 'Tax', and 'TotalWithTax' for each orderdetails row (via a function returning a Series), then use concat()
#     to merge these new columns back into the original orderdetails.
def summarize_row(row):
    subtotal = row['UnitPrice'] * row['OrderQty']
    tax = 0.07 * subtotal
    return pd.Series({
        'Subtotal': subtotal,
        'Tax': tax,
        'TotalWithTax': subtotal + tax})
summary_df = orderdetails.apply(summarize_row, axis=1)
orderdetails = pd.concat([orderdetails, summary_df], axis=1)