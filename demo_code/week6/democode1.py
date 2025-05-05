# ------------------------------------------------------------
# 0 Imports & set-up
# ------------------------------------------------------------
import pandas as pd
import numpy as np

pd.set_option("display.max_columns", 0)      # keep printed output tidy
pd.set_option("display.width", 120)


# ------------------------------------------------------------
# 1 Load the pipe-delimited files
# ------------------------------------------------------------

customers   = pd.read_csv("C:\\courses\\reposource\\ACCpython202503\\datasets\\customers.csv",   sep="|", encoding="latin1")
orderdetail = pd.read_csv("C:\\courses\\reposource\\ACCpython202503\\datasets\\orderdetails.csv", sep="|")
orderheader = pd.read_csv("C:\\courses\\reposource\\ACCpython202503\\datasets\\orderheader.csv", sep="|")
product     = pd.read_csv("C:\\courses\\reposource\\ACCpython202503\\datasets\\product.csv",      sep="|")

print("customers →", customers.shape,
      "orderdetail →", orderdetail.shape,
      "orderheader →", orderheader.shape,
      "product →", product.shape)

# ------------------------------------------------------------
# 2 Missing-data mechanics (NaN / pd.NA)
# ------------------------------------------------------------

# -- quick audit
for name, df in {"customers": customers,
                 "orderheader": orderheader,
                 "product": product}.items():
    print(f"{name:<12} missing cells → {df.isna().sum().sum():>4}")

# ― Three-value logic demo (True / False / NaN) ―
mask_gt_100 = product["ListPrice"] > 100          # comparison against NaN yields NaN
print("\nBoolean result contains NaN where ListPrice itself is NaN →")
print(mask_gt_100.head(8))


# ― Locate & count NaNs ―

print(product[["Size", "Weight"]].isna().sum())       # per-column count

# ― Cleaning options ―

clean_prod = (product
              .assign(Size = product["Size"].replace("", np.nan))     # recode
              .fillna({"Color":   "Unknown",                         # scalar fill
                       "Weight":  product["Weight"].median()})       # numeric fill
              .fillna(method="ffill",  limit=2)                      # forward-fill
              .fillna(method="bfill")                                # back-fill
              .interpolate(subset=["Weight"],                        # linear interpolate
                           limit_direction="both"))
print(clean_prod[["Color", "Size", "Weight"]].head())

# ― Dropping rows with critical nulls ―
order_no_cc = orderheader.dropna(subset=["CreditCardApprovalCode"])
print("\nRows kept after dropping NULL credit approvals →", len(order_no_cc))

# ― Calculations automatically skip NaNs unless skipna=False ―

print("Mean list price (skip Na):", product["ListPrice"].mean())
print("Mean list price (do NOT skip Na):",
      product["ListPrice"].mean(skipna=False))

# ― pd.NA & nullable dtypes ―

qty_nullable = orderdetail["OrderQty"].astype("Int64")          # capital “I”
print(pd.concat([qty_nullable.head(), pd.Series([pd.NA], dtype="Int64")]))

# ------------------------------------------------------------
# 3c  Practical categorical examples using your datasets
# ------------------------------------------------------------


# -----------------------------------------------------------------
# EXAMPLE A  ▸  Ordered categorical for garment size
# -----------------------------------------------------------------
size_order = ["XS", "S", "M", "L", "XL", "XXL"]           # business logic order

product["Size"] = (product["Size"]
                   .fillna("Unknown")                     # avoid NaN first
                   .astype("category")
                   .cat.set_categories(size_order + ["Unknown"], ordered=True))

print("Size categories (ordered):", list(product["Size"].cat.categories), "\n")

# • Sorting respects business order now
print("Sample sorted by Size:")
print(product[["ProductID", "Name", "Size"]].sort_values("Size").head(), "\n")

# -----------------------------------------------------------------
# EXAMPLE B  ▸  Consolidate colours into fewer labels
# -----------------------------------------------------------------
def simplify_color(c):
    """Collapse multicolour descriptions into 'Multi'."""
    if pd.isna(c):
        return "Unknown"
    return "Multi" if "/" in c else c.strip()

# Step 1  – operate on *object* dtype so we can create duplicates safely
simplified = product["Color"].astype("object").apply(simplify_color)

# Step 2  – cast back to category (pandas will auto-deduplicate)
product["ColorSimple"] = simplified.astype("category")

print("Original distinct colours   :", product["Color"].nunique(dropna=True))
print("Simplified colour categories:", list(product["ColorSimple"].cat.categories), "\n")

# • Quick profiling: how popular is each colour after simplification?
print(product["ColorSimple"].value_counts(dropna=False).head())

# -----------------------------------------------------------------
# BONUS  ▸  Numeric codes & efficient joins
# -----------------------------------------------------------------
product["ColorCode"] = product["ColorSimple"].cat.codes      # 0-based ints
print("\nHead with codes:")
print(product[["ColorSimple", "ColorCode"]].head())

# ------------------------------------------------------------
# 4 String & text operations
# ------------------------------------------------------------

cust = customers.copy()

# — Subset & slice phone numbers —
phones_tx = cust[cust["Phone"].str.startswith("2")]

# — Common string methods —
cust["EmailLower"] = cust["EmailAddress"].str.lower()
cust["Company_Prefix"] = cust["CompanyName"].str.slice(stop=10)

# — f-strings / formatted values inside `assign` / `apply` —
cust["FormalName"] = cust.apply(
        lambda r: f"{r['Title']} {r['LastName']}" 
                  if pd.notna(r['Title']) else r['LastName'], axis=1)

# — Simple regex: validate US-style phone “###-###-####” —
pattern = r"^\d{3}-\d{3}-\d{4}$"
cust["PhoneValid"] = cust["Phone"].str.match(pattern)
print(cust[["Phone","PhoneValid"]].head())

# ------------------------------------------------------------
# 5 Date, time, timedelta, time-zones
# ------------------------------------------------------------

oh = orderheader.copy()

# Convert to datetime
oh["OrderDate"] = pd.to_datetime(oh["OrderDate"])
oh["ShipDate"]  = pd.to_datetime(oh["ShipDate"])

# Compute shipping turnaround time
oh["ShipDays"] = (oh["ShipDate"] - oh["OrderDate"]).dt.days
print(oh[["OrderDate","ShipDate","ShipDays"]].head())

# Datetime components
oh["Quarter"] = oh["OrderDate"].dt.quarter

# Time-zones: assume OrderDate given in US Central, convert to UTC
central       = oh["OrderDate"].dt.tz_localize("America/Chicago")
oh["OrderDate_UTC"] = central.dt.tz_convert("UTC")
print("\nTime-zone convert preview:")
print(oh[["OrderDate","OrderDate_UTC"]].head())





# ------------------------------------------------------------
# 2b  Deeper missing-data techniques
# ------------------------------------------------------------


# ❶  value_counts INCLUDING NaNs (helpful QA metric)
print("Color frequencies (NaN kept):")
print(product["Color"].value_counts(dropna=False).head(), "\n")

# ❷  .where() — retain good rows, turn the rest to NaN
high_price = product["ListPrice"].where(product["ListPrice"] > 500)
print("Using .where to blank out low prices:\n", high_price.head())

# ❸  combine_first — hierarchy of data sources
alt_weight = product["Weight"].fillna(0)           # pretend this came from elsewhere
merged_weight = product["Weight"].combine_first(alt_weight)
print("\ncombined Weight is identical?", merged_weight.equals(alt_weight))

# ❹  Conditional fill: use median *by* Size category
prod2 = product.copy()
prod2["Weight"] = prod2.groupby("Size")["Weight"].transform(
                      lambda s: s.fillna(s.median()))
print("\nWeight nulls after group-wise median fill →",
      prod2["Weight"].isna().sum())

# ❺  Interpolation with method='polynomial'
poly = product.sort_values("ListPrice")["ListPrice"].interpolate(
            method="polynomial", order=2)
print("\nPolynomial interpolation example:", poly.head(8).values)

# ------------------------------------------------------------
# 3b  Extra dtype / categorical examples
# ------------------------------------------------------------


# ❶  Create NEW category level on the fly
product["Size"] = product["Size"].cat.add_categories("OneSize")
product.loc[product["Size"].isna(), "Size"] = "OneSize"

# ❷  cat.codes provides numeric surrogate keys
print("First 5 size codes:", product["Size"].cat.codes.head().tolist())

# ❸  downcast float to smallest viable subtype for memory demo
before_mem = product["ListPrice"].memory_usage(deep=True)
product["ListPrice"] = pd.to_numeric(product["ListPrice"],
                                     downcast="float")
after_mem = product["ListPrice"].memory_usage(deep=True)
print(f"ListPrice column RAM: {before_mem/1e3:.1f} KB → {after_mem/1e3:.1f} KB")

# ❹  astype w/ dict to convert many columns in one go

cust2 = customers.astype({"Title":      "string",
                          "MiddleName": "string",
                          "Phone":      "string"})
print("Mixed dtype conversion complete — sample dtypes:\n",
      cust2.dtypes.head(6))

# ------------------------------------------------------------
# 4b  Richer string / text operations
# ------------------------------------------------------------


#  Regex extract() — grab area code
customers["AreaCode"] = customers["Phone"].str.extract(r"^(\d{3})")
print(customers[["Phone", "AreaCode"]].head())

#  contains & case normalization
gmail_users = customers["EmailAddress"].str.lower().str.contains("@gmail")
print("\nGmail ratio:", gmail_users.mean().round(3))

#  str.split & explode to normalise multivalued column
prod3 = product.copy()
prod3["Tags"] = prod3["Color"].str.replace("/", "|", regex=False)   # fake tag list
prod_tags = (prod3
             .assign(Tags=prod3["Tags"].str.split("|"))
             .explode("Tags")
             .reset_index(drop=True))
print("\nExploded Tags preview:\n", prod_tags[["ProductID", "Tags"]].head())

#  vectorised number-to-string formatting
product["PriceFmt"] = product["ListPrice"].map("${:,.2f}".format)
print("\nFormatted price example:", product["PriceFmt"].head(3).tolist())

# str.get_dummies for one-hot encoding
color_OHE = product["Color"].str.get_dummies()
print("\nOne-hot columns created:", color_OHE.columns.tolist()[:5], "...")

# ------------------------------------------------------------
# 5b  Expanded datetime / timedelta demos
# ------------------------------------------------------------


# ❶  Resample: daily → weekly revenue
daily_rev = (orderdetail
             .merge(orderheader[["SalesOrderID", "OrderDate"]],
                    on="SalesOrderID")
             .assign(OrderDate=lambda d: pd.to_datetime(d["OrderDate"]))
             .groupby("OrderDate")["LineTotal"].sum())
weekly_rev = daily_rev.resample("W").sum()
print("First weekly totals:\n", weekly_rev.head())

# ❷  Rolling 4-week mean
weekly_rev_roll = weekly_rev.rolling(window=4).mean()
print("\n4-week rolling mean preview:", weekly_rev_roll.head(8).values)

# ❸  shift & pct_change for lag analysis
weekly_pct = weekly_rev.pct_change().round(3)
print("\nWeek-over-week % change:", weekly_pct.head(6).tolist())

# ❹  Business-day offsets
from pandas.tseries.offsets import BDay
next_bday = oh["OrderDate"] + BDay(1)
print("\nFirst few next business days:\n", next_bday.head())

# ❺  between_time: pick orders processed during office hours
oh = oh.set_index("OrderDate")          # use OrderDate as index for demo
office = oh.between_time("08:00", "17:00")
print("\nOrders logged 08-17h →", len(office), "rows")

# ❻  floor / ceil to nearest hour
orderheader["OrderHour"] = pd.to_datetime(
                             orderheader["OrderDate"]).dt.floor("h")
print("\nOrderHour col preview:", orderheader["OrderHour"].head())