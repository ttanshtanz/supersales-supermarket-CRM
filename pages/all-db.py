import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('users.db')
c = conn.cursor()

# # Create a table to store user information
# c.execute('''
#     CREATE TABLE IF NOT EXISTS users (
#         id INTEGER PRIMARY KEY,
#         username TEXT UNIQUE,
#         email TEXT UNIQUE,
#         password TEXT,
#         state INTEGER DEFAULT 0,
#         designation TEXT,
#         residing_state TEXT
#     )
# ''')

# # Create the products table
# c.execute('''
#     CREATE TABLE IF NOT EXISTS products (
#         product_id INTEGER PRIMARY KEY,
#         seller_id INTEGER,
#         product_category TEXT,
#         product_name TEXT,
#         product_brand TEXT,
#         product_weight_g FLOAT,
#         product_length_cm FLOAT,
#         product_width_cm FLOAT,
#         product_height_cm FLOAT,
#         price FLOAT,
#         quantity INT,
#         image1 BLOB,
#         image2 BLOB,
#         image3 BLOB,
#         FOREIGN KEY (seller_id) REFERENCES users (id)
#     )
# ''')

# # Store image data as BLOB (Binary Large OBject)

# # Create the orders table
# c.execute('''
#     CREATE TABLE IF NOT EXISTS orders (
#         order_id INTEGER PRIMARY KEY,
#         customer_id INTEGER,
#         seller_id INTEGER,
#         product_id INTEGER,
#         quantity INT,  
#         order_status TEXT,
#         address TEXT,
#         phone TEXT,
#         total_charge FLOAT,
#         payment_method TEXT,
#         order_purchase_timestamp DATETIME,
#         FOREIGN KEY (product_id) REFERENCES products (product_id),
#         FOREIGN KEY (customer_id) REFERENCES users (id),            
#         FOREIGN KEY (seller_id) REFERENCES users (id)
#     )
# ''')

# # Create the review table
# c.execute('''
#     CREATE TABLE IF NOT EXISTS review (
#         review_id INTEGER PRIMARY KEY,
#         order_id INTEGER, 
#         order_status TEXT,
#         review_score FLOAT,
#         review_comment_message TEXT,
#         sentiment_result TEXT,
#         review_timestamp DATETIME,
#         FOREIGN KEY (order_id) REFERENCES orders (order_id)
#     )
# ''')

# # Create the cart table
# c.execute('''
#     CREATE TABLE IF NOT EXISTS shopping_cart (
#         cart_id INTEGER PRIMARY KEY,
#         user_id INTEGER, 
#         product_id INTEGER,
#         quantity INT, 
#         FOREIGN KEY (user_id) REFERENCES users (id),
#         FOREIGN KEY (product_id) REFERENCES products (product_id)
#     )
# ''')

# # Commit the changes and close the connection
# conn.commit()
# conn.close()

# /////////////////////////////////////////////////////////////////////////

# Add the new columns to the table

# c.execute('''
#     ALTER TABLE orders ADD COLUMN quantity INT
# ''')

# conn.commit()
# conn.close()

# /////////////////////////////////////////////////////////////////////////

# # # Add the new columns to the table

# c.execute('''
#     DELETE from review
# ''')

# conn.commit()
# conn.close()


# /////////////////////////////////////////////////////////////////////////

c.execute('''
     SELECT *
        FROM orders
          WHERE order_id = 6
          
''')

# Fetch all results
rows = c.fetchall()

# Process the results (print them in this case)
for row in rows[:10]:
    print(row)

# Close the connection
conn.commit()
conn.close()

# /////////////////////////////////////////////////////////////////////////

# # Add the new columns to the table

# c.execute('''
#     ALTER TABLE orders
#     RENAME COLUMN shipping_charge TO total_charge;
# ''')

# conn.commit()
# conn.close()

# ////////////////////////////////////////////////////////////////

# # SQL query to update the designation of the user with the specified email
# update_query = '''
#     UPDATE orders
#     SET order_id = 7
#     WHERE customer_id = 5
# '''

# # Execute the query with the email parameter
# c.execute(update_query)

# # Commit the changes
# conn.commit()

# # Close the connection
# conn.close()

# print("User designation updated successfully.")

# # ///////////////////////////////////////////////////////////////

# # Use PRAGMA table_info to describe the table structure
# c.execute('PRAGMA table_info(orders)')
# columns_info = c.fetchall()

# # Print or process the columns information
# for column in columns_info:
#     print(column)

# conn.commit()
# conn.close()