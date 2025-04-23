import pandas as pd

# ───────────────────────────────────────────────────────────────────────────────
# A. READ PIPE-DELIMITED FILES (if not already loaded)
# ───────────────────────────────────────────────────────────────────────────────
customers    = pd.read_csv('/workspaces/ACCpython202503/datasets/customers.csv',    sep='|', encoding='latin1')
orderheader  = pd.read_csv('/workspaces/ACCpython202503/datasets/orderdetails.csv',  sep='|', encoding='latin1')
orderdetails = pd.read_csv('/workspaces/ACCpython202503/datasets/orderheader.csv', sep='|', encoding='latin1')
product      = pd.read_csv('/workspaces/ACCpython202503/datasets/product.csv',      sep='|', encoding='latin1')

# ───────────────────────────────────────────────────────────────────────────────
# 7. CUSTOMER DATA CLEANING & ENRICHMENT
# ───────────────────────────────────────────────────────────────────────────────

# 7.1 Normalize phone numbers: strip out all non-digits
customers['CleanPhone'] = customers['Phone'].apply(
    lambda p: ''.join(filter(str.isdigit, p))  # keep only '0'–'9'
)
# Demo: show before/after on a few rows

# 7.2 Extract area code from 10-digit phones (first 3 digits)
customers['AreaCode'] = customers['CleanPhone'].apply(
    lambda num: num[:3] if len(num) >= 10 else None
)
# Explains handling of unexpected lengths

# 7.3 Extract email domain (right of “@”)
customers['EmailDomain'] = customers['EmailAddress'].apply(
    lambda e: e.split('@')[-1].lower() if isinstance(e, str) and '@' in e else None
)
# Real-world: group sales by email provider later

# 7.4 Construct full customer name (handle missing middle names)
def make_full_name(row):
    parts = [row['Title'], row['FirstName']]
    if pd.notna(row['MiddleName']):
        parts.append(row['MiddleName'])
    parts.append(row['LastName'])
    return ' '.join(parts)

customers['FullName'] = customers.apply(make_full_name, axis=1)
# Demo: how apply() can glue multiple columns into one

# ───────────────────────────────────────────────────────────────────────────────
# 8. ORDER ANALYSIS & TIMING
# ───────────────────────────────────────────────────────────────────────────────

# 8.1 Flag high-value orders
#    threshold could be a business rule (e.g. > $1,000)
orderheader['OrderValueCategory'] = orderheader['TotalDue'].apply(
    lambda td: 'HighValue' if td > 1000 else 'Standard'
)

# 8.2 Compute shipping delay in days: ship date minus order date
orderheader['OrderDate'] = pd.to_datetime(orderheader['OrderDate'])
orderheader['ShipDate']  = pd.to_datetime(orderheader['ShipDate'])
orderheader['DaysToShip'] = orderheader.apply(
    lambda r: (r['ShipDate'] - r['OrderDate']).days,
    axis=1
)
# Students can histogram DaysToShip to spot slow shipments

# 8.3 Identify late deliveries: shipped after the promised due date
orderheader['DueDate'] = pd.to_datetime(orderheader['DueDate'])
orderheader['DaysLate'] = orderheader.apply(
    lambda r: (r['ShipDate'] - r['DueDate']).days,
    axis=1
)
orderheader['IsLate'] = orderheader['DaysLate'].apply(
    lambda d: True if d > 0 else False
)

# ───────────────────────────────────────────────────────────────────────────────
# 9. PRODUCT & PROFITABILITY CALCULATION
# ───────────────────────────────────────────────────────────────────────────────

# 9.1 Categorize products by price tier
def price_tier(price):
    if price < 20:
        return 'Budget'
    elif price < 100:
        return 'Midrange'
    else:
        return 'Premium'

product['PriceTier'] = product['ListPrice'].apply(price_tier)
# Demo: how marketing might segment products

# 9.2 Compute line-item profit by merging product cost with sales
#    Merge orderdetails with product’s StandardCost & ListPrice
merged = orderdetails.merge(
    product[['ProductID','StandardCost','ListPrice']],
    on='ProductID',
    how='left'
)

# Apply per-row profit calculation = (ListPrice − StandardCost) × OrderQty
merged['LineProfit'] = merged.apply(
    lambda r: (r['ListPrice'] - r['StandardCost']) * r['OrderQty'],
    axis=1
)
# Reveal which SKUs drive the most margin

# 9.3 Calculate cost-to-price ratio for each product (inspection)
product['CostToPriceRatio'] = product.apply(
    lambda r: r['StandardCost'] / r['ListPrice'],
    axis=1
)
# Helpful for purchasing negotiations

# ───────────────────────────────────────────────────────────────────────────────
# 10. DATAFRAME INSPECTION & FORMATTING
# ───────────────────────────────────────────────────────────────────────────────

# 10.1 Count missing values per column in customers
missing_counts = customers.apply(lambda col: col.isna().sum())
# Students see which fields need data cleansing

# 10.2 Format all floats in merged to 2 decimal places (applymap)
merged_formatted = merged.applymap(
    lambda x: f"{x:.2f}" if isinstance(x, float) else x
)
# Demo the difference between raw numbers vs. formatted strings

# ───────────────────────────────────────────────────────────────────────────────
# Wrap-up: encourage students to tweak thresholds, try vectorized
# replacements (e.g. df['DaysToShip'].dt.days), and time large apply() vs.
# pure vectorized ops for performance discussions.
