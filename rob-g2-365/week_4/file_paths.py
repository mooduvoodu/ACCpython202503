from pathlib import Path
import pandas as pd

CUSTOMER_FILE = 'customers.csv'
PRODUCT_FILE ='product.csv'
ORDERHEADER_FILE = 'orderheader.csv'
ORDERDETAILS_FILE = 'orderdetails.csv'
ROOTPATH = Path('../../datasets')

CUSTOMER_PATH = ROOTPATH.joinpath(CUSTOMER_FILE)
PRODUCT_PATH = ROOTPATH.joinpath(PRODUCT_FILE)
ORDERHEADER_PATH = ROOTPATH.joinpath(ORDERHEADER_FILE)
ORDERDETAILS_PATH = ROOTPATH.joinpath(ORDERDETAILS_FILE)

CSV_FILES = [CUSTOMER_PATH, PRODUCT_PATH, ORDERHEADER_PATH, ORDERDETAILS_PATH]

def read_customers():
  return pd.read_csv(CUSTOMER_PATH, sep='|', encoding='latin1')

def read_products():
  return pd.read_csv(PRODUCT_PATH, sep='|', encoding='latin1')

def read_order_headers():
  return pd.read_csv(ORDERHEADER_PATH, sep='|', encoding='latin1')

def read_order_details():
  return pd.read_csv(ORDERDETAILS_PATH, sep='|', encoding='latin1')

