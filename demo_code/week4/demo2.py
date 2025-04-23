import pandas as pd

# ───────────────────────────────────────────────────────────────────────────────
# A. LOAD PIPE-DELIMITED FILES
#    Read each CSV using sep='|' and latin1 encoding to avoid Unicode errors.
# ───────────────────────────────────────────────────────────────────────────────
customers    = pd.read_csv('/workspaces/ACCpython202503/datasets/customers.csv',
                           sep='|', encoding='latin1')
orderheader  = pd.read_csv('/workspaces/ACCpython202503/datasets/orderheader.csv',
                           sep='|', encoding='latin1')
orderdetails = pd.read_csv('/workspaces/ACCpython202503/datasets/orderdetails.csv',
                           sep='|', encoding='latin1')
product      = pd.read_csv('/workspaces/ACCpython202503/datasets/product.csv',
                           sep='|', encoding='latin1')

# Rename stray column name if needed (sometimes trailing commas slip in)
if 'rowguid,' in product.columns:
    product = product.rename(columns={'rowguid,': 'rowguid'})


# ───────────────────────────────────────────────────────────────────────────────
# PRE-CALCULATION: CALCULATE TOTAL SPENT PER CUSTOMER
#    We need a TotalSpent field before we can flag VIPs.
# ───────────────────────────────────────────────────────────────────────────────
customer_spend = (
    orderheader
    .groupby('CustomerID', as_index=False)['TotalDue']
    .sum()                              # sum all orders per customer
    .rename(columns={'TotalDue':'TotalSpent'})
)
# Merge back into customers; those without orders become NaN → fill with 0
customers = customers.merge(customer_spend, on='CustomerID', how='left')
customers['TotalSpent'] = customers['TotalSpent'].fillna(0)


# ───────────────────────────────────────────────────────────────────────────────
# 2. SINGLE-COLUMN SERIES APPLY EXAMPLES
#    Demonstrate apply() on a single Series to transform each element.
# ───────────────────────────────────────────────────────────────────────────────

# 2.1 Compute the length of each FirstName
customers['FirstName_Length'] = customers['FirstName'].apply(len)

# 2.2 Title-case each first name using a custom function
def title_case(name):
    return name.title()                # capitalizes each word
customers['FirstName_Titled'] = customers['FirstName'].apply(title_case)

# 2.3 Flag “VIP” customers if TotalSpent > $1,000, else “Standard”
customers['CustomerStatus'] = customers['TotalSpent'].apply(
    lambda spent: 'VIP' if spent > 1000 else 'Standard'
)

# 2.4 Parse OrderDate strings into datetime and then extract the month
#     apply(pd.to_datetime) first, then .apply(lambda dt: dt.month)
orderheader['OrderDate']  = orderheader['OrderDate'].apply(pd.to_datetime)
orderheader['OrderMonth'] = orderheader['OrderDate'].apply(lambda dt: dt.month)


# ───────────────────────────────────────────────────────────────────────────────
# 3. MULTI-COLUMN APPLY (axis=1) EXAMPLES
#    Use apply(axis=1) to work with entire rows (Series) at once.
# ───────────────────────────────────────────────────────────────────────────────

# 3.1 Compute LineTotal = UnitPrice × OrderQty
#     Note: the column in our data is 'OrderQty', not 'Quantity'
orderdetails['LineTotal'] = orderdetails.apply(
    lambda row: row['UnitPrice'] * row['OrderQty'],
    axis=1
)

# 3.2 Apply a 10% discount on any line whose subtotal > $100
def apply_discount(row):
    subtotal = row['UnitPrice'] * row['OrderQty']
    discount = 0.10 * subtotal if subtotal > 100 else 0
    return subtotal - discount

orderdetails['DiscountedTotal'] = orderdetails.apply(apply_discount, axis=1)

# 3.3 Return multiple new columns via a Series from apply()
def summarize_row(row):
    subtotal = row['UnitPrice'] * row['OrderQty']
    tax = 0.07 * subtotal                # flat 7% tax
    return pd.Series({
        'Subtotal': subtotal,
        'Tax': tax,
        'TotalWithTax': subtotal + tax
    })

summary_df = orderdetails.apply(summarize_row, axis=1)
# Concatenate the summary DataFrame back onto the original
orderdetails = pd.concat([orderdetails, summary_df], axis=1)


# ───────────────────────────────────────────────────────────────────────────────
# 4. DATAFRAME-LEVEL APPLY
#    When apply() is called on a DataFrame, it iterates over columns by default.
# ───────────────────────────────────────────────────────────────────────────────

column_dtypes = customers.apply(lambda col: col.dtype)
# column_dtypes is a Series mapping each column name → its dtype


# ───────────────────────────────────────────────────────────────────────────────
# 5. ELEMENT-WISE APPLYMAP
#    applymap() runs a function on every single cell in the DataFrame.
# ───────────────────────────────────────────────────────────────────────────────

product_lower = product.applymap(
    lambda x: x.lower() if isinstance(x, str) else x
)
# Lowercases all text cells, leaves numbers and dates untouched


# ───────────────────────────────────────────────────────────────────────────────
# 7. CUSTOMER DATA CLEANING & ENRICHMENT
#    More real-world fixes: phone normalization, email parsing, full name.
# ───────────────────────────────────────────────────────────────────────────────

# 7.1 Strip non-digits out of phone numbers
customers['CleanPhone'] = customers['Phone'].apply(
    lambda p: ''.join(filter(str.isdigit, p)) if isinstance(p, str) else None
)

# 7.2 Extract the area code (first 3 digits) if we have at least 10 digits
customers['AreaCode'] = customers['CleanPhone'].apply(
    lambda num: num[:3] if isinstance(num, str) and len(num) >= 10 else None
)

# 7.3 Pull the domain part of each email (after the ‘@’)
customers['EmailDomain'] = customers['EmailAddress'].apply(
    lambda e: e.split('@')[-1].lower() if isinstance(e, str) and '@' in e else None
)

# 7.4 Build FullName by concatenating Title, First, Middle, Last—skipping blanks
def make_full_name(row):
    parts = []
    for fld in ['Title','FirstName','MiddleName','LastName']:
        val = row.get(fld)
        if pd.notna(val):
            txt = str(val).strip()
            if txt:
                parts.append(txt)
    return ' '.join(parts)

customers['FullName'] = customers.apply(make_full_name, axis=1)


# ───────────────────────────────────────────────────────────────────────────────
# 8. ORDER ANALYSIS & TIMING
#    Calculate shipping delays and late flags.
# ───────────────────────────────────────────────────────────────────────────────

# Convert any date columns safely (invalid → NaT)
for dtcol in ['ShipDate','DueDate']:
    if dtcol in orderheader.columns:
        orderheader[dtcol] = pd.to_datetime(orderheader[dtcol], errors='coerce')

# 8.1 Days to ship = ShipDate – OrderDate
orderheader['DaysToShip'] = orderheader.apply(
    lambda r: (r['ShipDate'] - r['OrderDate']).days
              if pd.notna(r.get('ShipDate')) and pd.notna(r.get('OrderDate'))
              else None,
    axis=1
)

# 8.2 Days late = ShipDate – DueDate, then flag late ones
orderheader['DaysLate'] = orderheader.apply(
    lambda r: (r['ShipDate'] - r['DueDate']).days
              if pd.notna(r.get('ShipDate')) and pd.notna(r.get('DueDate'))
              else None,
    axis=1
)
orderheader['IsLate'] = orderheader['DaysLate'].apply(
    lambda d: isinstance(d, (int,float)) and d > 0
)


# ───────────────────────────────────────────────────────────────────────────────
# 9. PRODUCT & PROFITABILITY CALCULATION
#    Segment products and calculate line-item profits.
# ───────────────────────────────────────────────────────────────────────────────

# 9.1 Assign Budget/Midrange/Premium tiers based on ListPrice
product['PriceTier'] = product['ListPrice'].apply(
    lambda price: 'Budget' if price < 20
                  else ('Midrange' if price < 100 else 'Premium')
)

# 9.2 Merge costs into orderdetails and compute line profit
merged = orderdetails.merge(
    product[['ProductID','StandardCost','ListPrice']],
    on='ProductID', how='left'
)
merged['LineProfit'] = merged.apply(
    lambda r: (r['ListPrice'] - r['StandardCost']) * r['OrderQty'], axis=1
)

# 9.3 Compute cost-to-price ratio for each product
product['CostToPriceRatio'] = product.apply(
    lambda r: (r['StandardCost'] / r['ListPrice'])
              if (isinstance(r['StandardCost'], (int,float)) and
                  isinstance(r['ListPrice'], (int,float)) and
                  r['ListPrice'] != 0)
              else None,
    axis=1
)


# ───────────────────────────────────────────────────────────────────────────────
# 10. DATAFRAME INSPECTION & FORMATTING
#    Quick checks on missing data and numeric formatting.
# ───────────────────────────────────────────────────────────────────────────────

missing_counts   = customers.apply(lambda col: col.isna().sum())
merged_formatted = merged.applymap(
    lambda x: f"{x:.2f}" if isinstance(x, float) else x
)






# Quick map of key columns:
# customers:    CustomerID, FirstName, LastName, …
# orderheader:  SalesOrderID, CustomerID, SalesOrderNumber, TotalDue, …
# orderdetails: SalesOrderID, SalesOrderDetailID, OrderQty, ProductID, UnitPrice, …
# product:      ProductID, Name, StandardCost, ListPrice, …

# Ensure IDs are present and non-null for joins
orderheader  = orderheader.dropna(subset=['SalesOrderID','CustomerID'])
orderdetails = orderdetails.dropna(subset=['SalesOrderID','ProductID'])
customers    = customers.dropna(subset=['CustomerID'])
product      = product.dropna(subset=['ProductID'])


# ───────────────────────────────────────────────────────────────────────────────
# 1. CONCATENATION EXAMPLES (pd.concat)
# ───────────────────────────────────────────────────────────────────────────────

# 1.1 Vertical concatenation (axis=0) of first 3 & last 3 orders
oh_top3 = orderheader.head(3)
oh_bot3 = orderheader.tail(3)
concat_vert = pd.concat([oh_top3, oh_bot3], axis=0, ignore_index=True)
# • Stacks rows from both subsets
# • ignore_index=True resets the index to 0–5

# 1.2 Vertical concat without resetting index (original indices preserved)
concat_vert_origidx = pd.concat([oh_top3, oh_bot3], axis=0, ignore_index=False)
# • You’ll see the original orderheader indices, possibly non-unique

# 1.3 Horizontal concatenation (axis=1) of customers & orders for same CustomerID
#    First, pick CustomerIDs present in both frames
common_ids = list(set(customers['CustomerID']) & set(orderheader['CustomerID']))
sample_ids = common_ids[:3]  # take any three that exist
#    Subset and set CustomerID as index for alignment
cust_sub = customers.set_index('CustomerID')[['FirstName','LastName']].loc[sample_ids]
oh_sub   = orderheader.set_index('CustomerID')[['SalesOrderNumber','TotalDue']].loc[sample_ids]
concat_horz = pd.concat([cust_sub, oh_sub], axis=1)
# • Joins side-by-side by matching index values
# • Rows = sample CustomerIDs; columns from both DataFrames

# 1.4 Concatenate rows with different columns (axis=0)
df_small_cust = customers[['CustomerID','FirstName']].head(2)
df_small_prod = product[['ProductID','Name']].head(2)
concat_diff_cols = pd.concat([df_small_cust, df_small_prod], axis=0, sort=False)
# • Rows from df_small_cust have NaN for ProductID/Name
# • Rows from df_small_prod have NaN for CustomerID/FirstName

# 1.5 Concatenate columns with different rows (axis=1)
#    Align df_small_cust (2 rows) with df_small_prod (2 rows) by index 0,1
concat_diff_rows = pd.concat([df_small_cust, df_small_prod], axis=1)
# • Columns side-by-side; if lengths differ, missing cells become NaN


# ───────────────────────────────────────────────────────────────────────────────
# 2. MERGE (JOIN) EXAMPLES
# ───────────────────────────────────────────────────────────────────────────────

# 2.1 INNER JOIN orderheader ↔ orderdetails on SalesOrderID
inner = pd.merge(
    orderheader,
    orderdetails[['SalesOrderID','OrderQty','UnitPrice']],
    on='SalesOrderID',
    how='inner'
)
# • Keeps only orders that have matching line items

# 2.2 LEFT JOIN orderdetails → product on ProductID
left = pd.merge(
    orderdetails,
    product[['ProductID','Name','ListPrice']],
    on='ProductID',
    how='left'
)
# • All line items retained; missing product info → NaN

# 2.3 RIGHT JOIN orderdetails → product on ProductID
right = pd.merge(
    orderdetails,
    product[['ProductID','Name']],
    on='ProductID',
    how='right'
)
# • All products retained; line items absent for some SKUs → NaN

# 2.4 FULL OUTER JOIN customers ↔ orderheader on CustomerID
full = pd.merge(
    customers[['CustomerID','FirstName','LastName']],
    orderheader[['CustomerID','SalesOrderNumber','TotalDue']],
    on='CustomerID',
    how='outer'
)
# • All customers & all orders; unmatched rows flagged by NaN

# 2.5 CROSS JOIN customers × product
cross = pd.merge(
    customers[['CustomerID']],
    product[['ProductID']],
    how='cross'
)
# • Cartesian product: every customer paired with every product
