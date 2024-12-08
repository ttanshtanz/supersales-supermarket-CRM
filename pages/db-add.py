import pandas as pd
import sqlite3

# Load the CSV
df = pd.read_csv('Data/New/order_data_dwld.csv')

# Convert columns
# df['order_id'] = df['order_id'].astype('Int64')
# df['customer_id'] = df['customer_id'].astype('Int64')
df['quantity'] = df['quantity'].astype(int)
df['total_charge'] = df['total_charge'].astype(float)
# df['order_purchase_timestamp'] = df['total_charge'].astype(float)

# Add missing columns with None values if not present in the DataFrame
df['seller_id'] = None
df['product_id'] = None
df['address'] = None
df['phone'] = None

# Drop duplicates based on 'order_id'
df = df.drop_duplicates(subset='order_id')

# Connect to SQLite database
conn = sqlite3.connect('users.db')

# Insert the data into the 'orders' table
df.to_sql('orders', conn, if_exists='append', index=False)

# Commit and close connection
conn.commit()
conn.close()
