import pandas as pd

# Task 1: Extract and Preview the Data
df = pd.read_csv(r"C:\Users\SHUBHA\Downloads\Superstore.csv")

# Q1 - Preview
print("Top 5 records:\n", df.head())
print("\nShape of the data (rows, columns):", df.shape)
print("\nColumn names and data types:\n", df.dtypes)

# Task 2: Clean Column Names and Normalize Dates
# Q2 - Clean headers
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('/', '_')

# Convert to datetime
df['order_date'] = pd.to_datetime(df['order_date'], dayfirst=True)
df['ship_date'] = pd.to_datetime(df['ship_date'], dayfirst=True)

# Task 3: Profitability by Region and Category
# Q3 - Group by region and category
region_category_profit = df.groupby(['region', 'category']).agg({
    'sales': 'sum',
    'profit': 'sum',
    'discount': 'mean'
}).reset_index()

print("\nRegion & Category Profitability:\n", region_category_profit)

# Find the most profitable Region+Category
most_profitable = region_category_profit.sort_values(by='profit', ascending=False).head(1)
print("\nMost Profitable Region + Category:\n", most_profitable)

# Task 4: Top 5 Most Profitable Products
# Q4
top_products = df.groupby('product_name')['profit'].sum().sort_values(ascending=False).head(5)
print("\nTop 5 Most Profitable Products:\n", top_products)

# Task 5: Monthly Sales Trend
# Q5 - Extract month and group
df['order_month'] = df['order_date'].dt.to_period('M')
monthly_sales = df.groupby('order_month')['sales'].sum().reset_index()
print("\nMonthly Sales Trend:\n", monthly_sales)

# Task 6: Cities with Highest Average Order Value
# Q6
df['order_value'] = df['sales'] / df['quantity']
city_order_value = df.groupby('city')['order_value'].mean().sort_values(ascending=False).head(10)
print("\nTop 10 Cities by Average Order Value:\n", city_order_value)

# Task 7: Identify and Save Orders with Loss
# Q7
loss_orders = df[df['profit'] < 0]
loss_orders.to_csv("loss_orders.csv", index=False)
print("\nLoss orders saved to loss_orders.csv")

# Task 8: Detect Null Values and Impute
# Q8
null_counts = df.isnull().sum()
print("\nMissing Values:\n", null_counts)

# Fill missing price values (if 'price' column exists)
if 'price' in df.columns:
    df['price'] = df['price'].fillna(1)
    print("\nMissing 'price' values filled with 1")
else:
    print("\nNo 'price' column found to fill missing values.")
