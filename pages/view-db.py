# Reading

import sqlite3
import pandas as pd
import streamlit as st

# Connect to SQLite database
conn = sqlite3.connect('users.db')
c = conn.cursor()

# Fetch all data from the users table
c.execute('SELECT * FROM users')
rows = c.fetchall()

# Get the column names
column_names = [description[0] for description in c.description]

# Convert to DataFrame
df_users = pd.DataFrame(rows, columns=column_names)

# Close the connection
conn.close()

# Display the DataFrame using Streamlit
st.write(df_users)
