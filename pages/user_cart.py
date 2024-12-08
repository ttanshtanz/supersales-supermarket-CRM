import streamlit as st
import pandas as pd
import os
import plotly.express as px
import sqlite3
import hashlib

# Initialize Streamlit
st.set_page_config(
    page_title="SuperSales",
    page_icon="💹",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ////////////////////////////////////////////////////////////////////////////////////////////////

# Function to load data and cache it
@st.cache_data  # Cache the returned dataframe
def load_data(file_path):
    return pd.read_csv(file_path)

# Get the directory of the current script
current_dir = os.path.dirname('app.py')
file_path = os.path.join(current_dir, 'Data/New/all_details.csv')
# Load the data
df = load_data(file_path)

# Get unique customer states
df = df.dropna(subset=['product_category'])
df['product_category'] = df['product_category'].astype(str)
product_categories = df['product_category'].unique()
product_categories.sort()

# ////////////////////////////////////////////////////////////////////////////////////////////////
# Function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to fetch logged-in user's information
def fetch_logged_in_user():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE state = 1')
    user = c.fetchone()
    conn.close()
    return user

# Function to update user state in the database
def update_user_state(username, state):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('UPDATE users SET state = ? WHERE username = ?', (state, username))
    conn.commit()
    conn.close()

def get_products():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        SELECT product_id, seller_id, product_category, product_name, product_brand, 
               product_weight_g, product_length_cm, product_width_cm, product_height_cm, 
               price, quantity, image1, image2, image3 
        FROM products
    ''')
    products = c.fetchall()
    conn.close()
    return products


def add_to_cart(user_id, product_id, quantity):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO shopping_cart (user_id, product_id, quantity)
        VALUES (?, ?, ?)
    ''', (user_id, product_id, quantity))
    conn.commit()
    conn.close()

def remove_from_cart(user_id, product_id):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        DELETE FROM shopping_cart WHERE user_id = ? AND product_id = ?
    ''', (user_id, product_id))
    conn.commit()
    conn.close()

def is_in_cart(user_id, product_id):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        SELECT * FROM shopping_cart WHERE user_id = ? AND product_id = ?
    ''', (user_id, product_id))
    item = c.fetchone()
    conn.close()
    return item is not None

def cart(user_id, product_id):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        SELECT * FROM shopping_cart WHERE user_id = ? AND product_id = ?
    ''', (user_id, product_id))
    item = c.fetchone()
    conn.close()
    return item

# Function to get cart count
def get_cart_count(user_id):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT SUM(quantity) FROM shopping_cart WHERE user_id = ?', (user_id,))
    count = c.fetchone()[0]
    conn.close()
    return count if count else 0

def fetch_user_designation(username):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT designation FROM users WHERE username = ?', (username,))
    designation = c.fetchone()[0]
    conn.close()
    return designation

# Check if user is logged in
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    user = fetch_logged_in_user()
    if user:
        st.session_state.logged_in = True
        st.session_state.user = user
    else:
        st.session_state.logged_in = False
        st.session_state.user = None

if not st.session_state.logged_in:
    st.warning("You need to login first!")
    st.switch_page('pages/user_login.py')
    st.stop()

# Logout functionality
def logout():
    if st.session_state.user:
        update_user_state(st.session_state.user[1], 0)
        st.session_state.logged_in = False
        st.session_state.user = None
        st.experimental_rerun()

# Function to fetch cart items for the logged-in user
def fetch_cart_items(user_id):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        SELECT p.product_id, p.seller_id, p.product_category, p.product_name, p.product_brand, 
               p.product_weight_g, p.product_length_cm, p.product_width_cm, p.product_height_cm, 
               p.price, c.quantity, p.image1, p.image2, p.image3
        FROM shopping_cart c
        JOIN products p ON c.product_id = p.product_id
        WHERE c.user_id = ?
    ''', (user_id,))
    cart_items = c.fetchall()
    conn.close()
    return cart_items

def calculate_total_price(user_id):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        SELECT p.price, c.quantity
        FROM shopping_cart c
        JOIN products p ON c.product_id = p.product_id
        WHERE c.user_id = ?
    ''', (user_id,))
    items = c.fetchall()
    conn.close()
    
    total_price = sum(price * quantity for price, quantity in items)
    return total_price

# Load custom CSS
st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">', unsafe_allow_html=True)
st.markdown('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">', unsafe_allow_html=True)

# Custom CSS for hiding Streamlit UI components
st.markdown(
    """
    <style>
    header.stButton > div.stButton > span {
        display: none !important;
    }
    .st-emotion-cache-18ni7ap, .st-emotion-cache-6qob1r eczjsme3, .st-emotion-cache-1ec6rqw eczjsme11{
        display: none !important;
        visibility: hidden;
    }
    .st-emotion-cache-vk3wp9{
        z-index: 0 !important;
    }
    .st-emotion-cache-1ww3bz2{
    gap: 0.54rem;
    }
    .reportview-container{
    background-color: white !important;
    }
    header {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    section[data-testid="stSidebarNav"]{
            display: none !important;
            visibility: hidden;
    }
    section[data-testid="stSidebarNav"][aria-expanded="true"]{
            display: none !important;
            visibility: hidden;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Function to load data and cache it
@st.cache_data  # Cache the returned dataframe
def load_data(file_path):
    return pd.read_csv(file_path)

# Navbar HTML with logout button
navbar_html = f"""
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css" rel="stylesheet">
<style>
    .navbar {{
        background-color: #00114a;
        color: white;
        z-index: 1000;
        padding: 0.5rem 1rem;
    }}
    .navbar-brand {{
        font-size: 1.2em;
        font-weight: bold;
        color: white !important;
    }}
    .navbar-nav .nav-link {{
        font-size: 1em;
        margin-left: 15px;
        margin-right: 15px;
        color: white !important;
        transition: color 0.3s ease-in-out, background-color 0.3s ease-in-out;
    }}
    .navbar-nav .nav-link:hover {{
        color: #cecece !important;
        background-color: rgba(255, 255, 255, 0.2);
        border-radius: 5px;
    }}
    .navbar-nav .nav-link.active {{
        font-weight: bold;
        background-color: rgba(255, 255, 255, 0.3);
        border-radius: 5px;
    }}
    .navbar-toggler {{
        border-color: rgba(255, 255, 255, 0.1);
    }}
    .navbar-toggler-icon {{
        background-image: url("data:image/svg+xml;charset=utf8,%3Csvg viewBox='0 0 30 30' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath stroke='rgba%2872, 118, 255, 1%29' stroke-width='2' linecap='round' linejoin='round' d='M4 7h22M4 15h22M4 23h22'/%3E%3C/svg%3E");
    }}
    .navbar-nav {{
        justify-content: flex-end;
    }}

    .h-title {{
        font-size: 1.4em;
        font-weight: bold;
        text-align: center;
        margin-bottom: 15px;
        background-color: #787878;
        color: white;
        margin-bottom: 15px;
        border-radius: 10px;
        padding: 3px;
    }}

    .st-emotion-cache-b1tq6m {{
        gap: 0rem;
    }}

    .st-emotion-cache-1tpl0xr e1nzilvr4 {{
        display: none;
    }}
</style>
"""
st.markdown(navbar_html, unsafe_allow_html=True)


# Navbar HTML with logout button
navbar_html = f"""
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css" rel="stylesheet">
<style>
    .navbar {{
        background-color: #00114a;
        color: white;
        z-index: 1000;
        padding: 0.5rem 1rem;
    }}
    .navbar-brand {{
        font-size: 1.2em;
        font-weight: bold;
        color: white !important;
    }}
    .navbar-nav .nav-link {{
        font-size: 1em;
        margin-left: 15px;
        margin-right: 15px;
        color: white !important;
        transition: color 0.3s ease-in-out, background-color 0.3s ease-in-out;
    }}
    .navbar-nav .nav-link:hover {{
        color: #cecece !important;
        background-color: rgba(255, 255, 255, 0.2);
        border-radius: 5px;
    }}
    .navbar-nav .nav-link.active {{
        font-weight: bold;
        background-color: rgba(255, 255, 255, 0.3);
        border-radius: 5px;
    }}
    .navbar-toggler {{
        border-color: rgba(255, 255, 255, 0.1);
    }}
    .navbar-toggler-icon {{
        background-image: url("data:image/svg+xml;charset=utf8,%3Csvg viewBox='0 0 30 30' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath stroke='rgba%2872, 118, 255, 1%29' stroke-width='2' linecap='round' linejoin='round' d='M4 7h22M4 15h22M4 23h22'/%3E%3C/svg%3E");
    }}
    .navbar-nav {{
        justify-content: flex-end;
    }}

    .h-title {{
        font-size: 1.4em;
        font-weight: bold;
        text-align: center;
        margin-bottom: 15px;
        background-color: #787878;
        color: white;
        margin-bottom: 15px;
        border-radius: 10px;
        padding: 3px;
    }}

    .st-emotion-cache-b1tq6m {{
        gap: 0rem;
    }}

    .st-emotion-cache-1tpl0xr e1nzilvr4 {{
        display: none;
    }}
</style>
"""
st.markdown(navbar_html, unsafe_allow_html=True)

# Navbar HTML with logout button
seller_navbar_html = f"""
<nav class="navbar navbar-expand-lg navbar-dark fixed-top" tabindex="-1" data-testid="stHeader">
  <a class="navbar-brand" href="/app" style="padding-left: 5px;"><i class="fas fa-chart-line"></i> <b>SuperSales</b></a>

  <div class="collapse navbar-collapse" id="navbarSupportedContent">
    <ul class="navbar-nav justify-content-center mx-auto">
      <li class="nav-item">
        <a class="nav-link active" href="/app" target="_self"><i class="fas fa-search"></i> Explore</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="/report" target="_self"><i class="fas fa-file-alt"></i> Reports</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="/products" target="_self"><i class="fas fa-shopping-bag"></i> Products</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="/users" target="_self"><i class="fas fa-shopping-cart"></i> Orders</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="/user_profile" target="_self"><i class="fas fa-user"></i> Profile</a>
      </li>
    </ul>
  </div>
    <div class="nav-item">
        <span class="navbar-brand"><b><a style='color:white; text-decoration:none; ' href="/user_profile" target="_self"><i class="fas fa-user-circle"></i> {st.session_state.user[1]}</a></b></span>
    </div>
</nav>
"""

# Navbar HTML with logout button
user_navbar_html = f"""
<nav class="navbar navbar-expand-lg navbar-dark fixed-top" tabindex="-1" data-testid="stHeader">
  <a class="navbar-brand" href="/app" style="padding-left: 5px;"><i class="fas fa-chart-line"></i> <b>SuperSales</b></a>

  <div class="collapse navbar-collapse" id="navbarSupportedContent">
    <ul class="navbar-nav justify-content-center mx-auto">
      <li class="nav-item">
        <a class="nav-link" href="/user_products" target="_self"><i class="fas fa-shopping-bag"></i> Shop</a>
      </li>
      <li class="nav-item">
        <a class="nav-link active" href="/user_cart" target="_self"><i class="fas fa-shopping-cart"></i> Cart</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="/user_products" target="_self"><i class="fas fa-luggage-cart"></i> Orders</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="/user_profile" target="_self"><i class="fas fa-user"></i> Profile</a>
      </li>
    </ul>
  </div>
    <div class="nav-item">
        <span class="navbar-brand"><a href="/user_cart" target="_self"><i class="fas fa-shopping-cart"></i></a>&nbsp;&nbsp;&nbsp;&nbsp;<b><a style='color:white; text-decoration:none; ' href="/user_profile" target="_self"><i class="fas fa-user-circle"></i> {st.session_state.user[1]}</a></b></span>
    </div>
</nav>
"""

# Navbar HTML with logout button
admin_navbar_html = f"""
<nav class="navbar navbar-expand-lg navbar-dark fixed-top" tabindex="-1" data-testid="stHeader">
  <a class="navbar-brand" href="/app" style="padding-left: 5px;"><i class="fas fa-chart-line"></i> <b>SuperSales</b></a>

  <div class="collapse navbar-collapse" id="navbarSupportedContent">
    <ul class="navbar-nav justify-content-center mx-auto">
      <li class="nav-item">
        <a class="nav-link active" href="/app" target="_self"><i class="fas fa-search"></i> Explore</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="/predict" target="_self"><i class="fas fa-chart-bar"></i> Predict</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="/chat" target="_self"><i class="fas fa-comments"></i> Chat</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="/review" target="_self"><i class="fas fa-star"></i> Reviews</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="/report" target="_self"><i class="fas fa-file-alt"></i> Reports</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="/users" target="_self"><i class="fas fa-user-plus"></i> Users</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="/user_profile" target="_self"><i class="fas fa-user"></i> Profile</a>
      </li>
    </ul>
  </div>
    <div class="nav-item">
        <span class="navbar-brand"><b><a style='color:white; text-decoration:none; ' href="/user_profile" target="_self"><i class="fas fa-user-circle"></i> {st.session_state.user[1]}</a></b></span>
    </div>
</nav>
"""

user_designation = fetch_user_designation(st.session_state.user[1])

if user_designation:
    if user_designation == 'Admin':
        st.markdown(admin_navbar_html, unsafe_allow_html=True)
    if user_designation == 'Seller':
        st.switch_page('pages/products.py')
        st.markdown(seller_navbar_html, unsafe_allow_html=True)
    if user_designation == 'Customer':
        st.markdown(user_navbar_html, unsafe_allow_html=True)

# /////////////////////////////////////////////////////////////////////////////////////////////////////////
st.markdown("""
<style>
	.stTabs [data-baseweb="tab-list"] {
		gap: 3rem;
    }
</style>""", unsafe_allow_html=True)

st.header("**Your Cart**")
st.write(" ")
user_id = st.session_state.user[0]
cart_items = fetch_cart_items(user_id)

# Calculate the total price of items in the cart
total_price = calculate_total_price(user_id)

if not cart_items:
    st.write("Your cart is empty. [Go to shop](user_products)")
else:
    # Get cart count for the current user
    user_id = st.session_state.user[0]
    cart_count = get_cart_count(user_id)
    c1, c2, c3, c4 = st.columns(4)
    # Display a warning message if there are items in the cart
    with c1:
        st.write(f"#### Subtotal: **{total_price} R$**")
    with c2:
        if cart_count > 0:
            if st.button(f"Proceed to Buy ({cart_count} item(s))", key="buy", type="primary"):
                st.switch_page('pages/user_buy.py')
    st.markdown("""<hr style="height:1px;border:none;color:#333;background-color:#333;width:90%;" /> """, unsafe_allow_html=True)

    # //////////////////////////////////////////////////////////////////////////////////////
    for item in cart_items:
        product_id, seller_id, product_category, product_name, product_brand, \
        product_weight_g, product_length_cm, product_width_cm, product_height_cm, \
        price, quantity, image1, image2, image3 = item
        
        col1, col2, col3, col4, col5, col6, col7, col8, col9 = st.columns([1, 3, 1, 2, 1, 1, 1, 1, 1])
        
        col2.write(product_name)
        col3.write(product_brand)
        col4.write(product_category)
        col5.write(f'{product_weight_g} g')
        col6.write(f'{product_length_cm} x {product_width_cm} x {product_height_cm} cm')
        col7.write(f'{price} R$')
        col8.write(f'{quantity} pcs')
        
        if image1:
            col1.image(image1, use_column_width=True)
        
        if col9.button("Delete", key=f"delete_{product_id}"):
            remove_from_cart(user_id, product_id)
            st.experimental_rerun()

        st.markdown("""<hr style="height:1px;border:none;color:#333;background-color:#333;width:90%;" /> """, unsafe_allow_html=True)
        
# /////////////////////////////////////////////////////////////////////////////////////////////////////////
# st.info('Credit: (aka [Data Professor](https://youtube.com/dataprofessor/))')
st.markdown(
    """
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
    """,
    unsafe_allow_html=True
)
st.markdown("""
<script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
""", unsafe_allow_html=True)