from file_paths import *
import pandas as pd

# Part 5: Simple Profiling
#   • Total rows per DataFrame
#   • Unique EmailAddress count in customers
#   • Rows with discount > 0 in order details
#   • value_counts of UnitPriceDiscount
#   • value_counts & percent of Status in order header
#   • Percent distribution of SalesPerson in customers
#   • Count of discontinued products (DiscontinuedDate not null)
#   • Average LineTotal in order details


#   • Total rows per DataFrame
for file in CSV_FILES:
  df = pd.read_csv(str(file), sep='|', encoding='latin-1')
  print(len(df))


#   • Unique EmailAddress count in customers
df = pd.read_csv(CUSTOMER_PATH, sep='|', encoding='latin-1')
print(df.columns)
print(df['EmailAddress'].unique())

#   • Rows with discount > 0 in order details
df = pd.read_csv(ORDERDETAILS_PATH, sep='|', encoding='latin-1')
print(df.columns)
print(df[df['UnitPriceDiscount'] >0])

#   • value_counts of UnitPriceDiscount
print(df['UnitPriceDiscount'].value_counts())

#   • value_counts & percent of Status in order header
df = pd.read_csv(ORDERHEADER_PATH, sep='|', encoding='latin-1')
print(df.columns)
value_counts_status = df['Status'].value_counts()
print(value_counts_status)
print(df['Status'].value_counts(normalize=True) )

#   • Percent distribution of SalesPerson in customers
df = pd.read_csv(CUSTOMER_PATH, sep='|', encoding='latin-1')
print(df['SalesPerson'].value_counts(normalize=True))

#   • Count of discontinued products (DiscontinuedDate not null)
df = pd.read_csv(PRODUCT_PATH, sep='|', encoding='latin-1')
print(len(df[df['DiscontinuedDate'].notnull()]))

#   • Average LineTotal in order details
df = pd.read_csv(ORDERDETAILS_PATH, sep='|', encoding='latin-1')
print(df['LineTotal'].mean())
