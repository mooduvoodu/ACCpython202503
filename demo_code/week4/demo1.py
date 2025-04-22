

import pandas as pd   # pandas is the primary library for tabular data manipulation
import numpy as np    # numpy provides numerical operations and random number generation
import os             # os allows us to interact with the operating system (e.g., checking file sizes)

# ───── Step 1: Seed for reproducibility ───────────────────────────────────────────
np.random.seed(0)
# By setting the seed, any call to numpy's random functions will
# produce the same “random” results each time this script runs.
# This is crucial for teaching, so students see consistent outputs.

# ───── Step 2: Build an ad‑hoc DataFrame with multiple datatypes ────────────────
data = {
    'int_col':   [1, 2, 3, 4],                                        # integers
    'float_col': [0.1, 0.2, 0.3, 0.4],                                # floating‑point numbers
    'bool_col':  [True, False, True, False],                         # boolean values
    'date_str':  ['2025-02-01', '2025-02-05', '2025-02-10', '2025-02-15'],  
    # date strings stored as object type, to demonstrate later conversion
    'cat_col':   pd.Categorical(['A', 'B', 'A', 'C']),               # categorical data type
    'obj_col':   ['foo', 'bar', 'baz', 'qux']                        # generic Python objects/strings
}
idx = ['row1', 'row2', 'row3', 'row4']  # custom index labels instead of default integer index
df = pd.DataFrame(data, index=idx)
# Now df has 4 rows labeled row1–row4 and columns with distinct Pandas-supported dtypes.

# ───── Step 3: Inspect the DataFrame’s structure ────────────────────────────────
print("=== Structure ===")
print("Index labels:", df.index)                 # shows the row labels
print("Column names:", df.columns.tolist())      # lists all column names
print("Underlying NumPy array:\n", df.values)    # the raw 2D array backing the DataFrame
print("Column data types:\n", df.dtypes)         # dtype for each column
print(df.info())                                 # concise summary: non-null counts & dtypes

# Demonstrate dtype conversion using astype()
df['bool_as_int']  = df['bool_col'].astype(int)  # True/False → 1/0
df['float_as_str'] = df['float_col'].astype(str) # convert floats to their string representations
print("\nAfter .astype() conversions, new dtypes:\n", df.dtypes)

# ───── Step 4: Common Series methods ─────────────────────────────────────────────
print("\n=== Series Methods ===")
print("Sum of integers:", df['int_col'].sum())            # adds up all elements in int_col
print("Mean of integers:", df['int_col'].mean())          # arithmetic average
print("Float summary:\n", df['float_col'].describe())     # count, mean, std, min/max, quartiles
print("Unique categories:", df['cat_col'].unique())       # shows each unique category in cat_col
print("True/False counts:\n", df['bool_col'].value_counts())  # frequency of each boolean value

# ───── Step 5: Convert string dates to datetime dtype ───────────────────────────
df['date_dt'] = pd.to_datetime(df['date_str'])
# pd.to_datetime parses the ISO-formatted strings into datetime64[ns] objects,
# enabling date-specific operations like filtering by date or extracting month.
print("\nAfter date conversion, dtypes:\n", df.dtypes)

# ───── Step 6: Auto‑alignment & broadcasting ────────────────────────────────────
# 6a. Aligned Series: additions match by index labels
s_align = pd.Series({'row1': 10, 'row2': 20, 'row3': 30, 'row4': 40})
df['aligned_add'] = df['int_col'] + s_align
# The addition pairs df['int_col'] and s_align values for the same row label.

# 6b. Misaligned Series: introduces NaN where labels don’t match
s_misal = pd.Series({'row1': 5, 'row3': 15, 'row5': 25})
df['misaligned_add'] = df['int_col'] + s_misal
# 'row2' and 'row4' become NaN (no matching index in s_misal), 'row5' ignored.

# 6c. Scalar broadcasting: same scalar applied to every element
df['scalar_mult'] = df['float_col'] * 100
# multiplies each float_col value by 100.

# 6d. DataFrame + DataFrame with shifted index
df2 = df[['int_col', 'float_col']].copy()
df2.index = ['row2','row3','row4','row5']  
# shift index down to demonstrate df + df2 alignment
df_df_add = df[['int_col','float_col']] + df2
print("\nDataFrame + DataFrame with different indices:\n", df_df_add)

# ───── Step 7: Selecting parts of the DataFrame ────────────────────────────────
subset_loc  = df.loc[['row1','row3'], ['int_col','obj_col']]
# .loc uses labels: select rows row1 & row3 and columns int_col & obj_col
subset_iloc = df.iloc[1:3, 0:3]
# .iloc uses integer positions: rows 1–2, columns 0–2
print("\nSubset using .loc:\n", subset_loc)
print("\nSubset using .iloc:\n", subset_iloc)

# Demonstrate reset_index to move labels into a column
df_reset = df.reset_index().rename(columns={'index':'orig_index'})
# original index becomes a new column called 'orig_index'; new integer index is assigned
print("\nAfter reset_index():\n", df_reset.head())

# ───── Step 8: Modify & add columns in-place ────────────────────────────────────
# Overwrite int_col with new random integers
df['int_col'] = np.random.randint(100, 200, size=len(df))
# Creates a new column from arithmetic between existing columns
df['sum_int_float'] = df['int_col'] + df['float_col']

# Use .assign() for chained additions without modifying original directly
df = df.assign(
    prod_int_float = lambda x: x['int_col'] * x['float_col'],
    neg_bool       = lambda x: ~x['bool_col']  # bitwise NOT flips True↔False
)

# Rename a column for clarity
df = df.rename(columns={'obj_col':'object_column'})

print("\nAfter in-place modifications and assign():\n", df.head())

# ───── Step 9: Dropping rows & columns ─────────────────────────────────────────
# Drop columns by name (axis=1)
df_drop_cols = df.drop(['misaligned_add','float_as_str'], axis=1)
# Drop a specific row by its label (axis=0)
df_drop_rows = df.drop(['row4'], axis=0)
print("\nAfter dropping columns:\n", df_drop_cols.head())
print("\nAfter dropping row 'row4':\n", df_drop_rows)

# ───── Step 10: Exporting & Importing (Pickle vs CSV) ──────────────────────────
pickle_path = '/workspaces/ACCpython202503/demo_code/week4/demo_df.pkl'
csv_path    = '/workspaces/ACCpython202503/demo_code/week4/demo_df.csv'

# to_pickle serializes the entire DataFrame (index, dtypes, data) to disk
df.to_pickle(pickle_path)
# to_csv writes a human-readable comma‑separated version (index=True writes row labels)
df.to_csv(csv_path)

print("\n=== File Sizes ===")
print("Pickle:", os.path.getsize(pickle_path), "bytes")
print("CSV:   ", os.path.getsize(csv_path), "bytes")

# Read back the files for verification
df_from_pkl = pd.read_pickle(pickle_path)
df_from_csv = pd.read_csv(csv_path, index_col=0, parse_dates=['date_dt'])
# parse_dates tells Pandas to convert the 'date_dt' column back to datetime dtype

print("\nDataFrame loaded from pickle:\n", df_from_pkl.head())
print("\nDataFrame loaded from CSV:\n", df_from_csv.head())




import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Reconstruct core DataFrame
np.random.seed(0)
data = {
    'int_col':   [1, 2, 3, 4],
    'float_col': [0.1, 0.2, 0.3, 0.4],
    'bool_col':  [True, False, True, False],
    'date_str':  ['2025-02-01', '2025-02-05', '2025-02-10', '2025-02-15'],
    'cat_col':   pd.Categorical(['A', 'B', 'A', 'C']),
    'obj_col':   ['foo', 'bar', 'baz', 'qux']
}
idx = ['row1', 'row2', 'row3', 'row4']
df = pd.DataFrame(data, index=idx)
df['date_dt'] = pd.to_datetime(df['date_str'])

# 1. Matplotlib: Line plot of int_col over custom index
plt.figure()
plt.plot(df.index, df['int_col'], marker='o')
plt.title('Matplotlib: int_col by Index')
plt.xlabel('Index')
plt.ylabel('int_col')
plt.show()

# 2. Seaborn: Scatter plot of float_col vs. int_col
plt.figure()
sns.scatterplot(x='int_col', y='float_col', data=df)
plt.title('Seaborn: float_col vs int_col')
plt.xlabel('int_col')
plt.ylabel('float_col')
plt.show()

# 3. Pandas: Histogram of float_col
plt.figure()
df['float_col'].plot(kind='hist')
plt.title('Pandas: Histogram of float_col')
plt.xlabel('float_col')
plt.show()
