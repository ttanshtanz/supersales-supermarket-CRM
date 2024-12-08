import streamlit as st
import pandas as pd
import os
import sqlite3
import hashlib
from datetime import datetime

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
df = df.dropna(subset=['seller_state'])
df['seller_state'] = df['seller_state'].astype(str)
customer_states = df['seller_state'].unique()
customer_states.sort()

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
        st.rerun()

# Function to fetch ordered items for the logged-in user
def fetch_orders(user_id):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        SELECT p.product_id, p.product_category, p.product_name, p.product_brand, 
               p.product_weight_g, p.price, c.order_id, c.order_status, c.address, c.phone, p.image1
        FROM orders c
        JOIN products p ON c.product_id = p.product_id
        WHERE c.seller_id = ? AND c.order_status != 'Cancelled'
        ORDER BY order_purchase_timestamp DESC
    ''', (user_id,))
    orders = c.fetchall()
    conn.close()
    return orders

def fetch_delivered_orders(user_id):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        SELECT p.product_id, p.product_category, p.product_name, p.product_brand, 
               p.product_weight_g, p.price, c.order_id, c.order_status, p.image1,
               r.review_score, r.review_comment_message, r.sentiment_result
        FROM orders c
        JOIN products p ON c.product_id = p.product_id
        LEFT JOIN review r ON c.order_id = r.order_id
        WHERE c.seller_id = ? AND c.order_status = 'Delivered'
        ORDER BY c.order_purchase_timestamp DESC
    ''', (user_id,))
    orders_with_reviews = c.fetchall()
    conn.close()
    return orders_with_reviews

def update_order_status(order_status, order_id):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        UPDATE orders SET order_status = ? WHERE order_id = ?
    ''', (order_status, order_id))
    conn.commit()
    conn.close()
    print(f'Order ID {order_id} status updated to {order_status}')

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
        <a class="nav-link" href="/seller_dashboard" target="_self"><i class="fas fa-search"></i> Explore</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="/products" target="_self"><i class="fas fa-shopping-bag"></i> Products</a>
      </li>
      <li class="nav-item">
        <a class="nav-link active" href="/seller_orders" target="_self"><i class="fas fa-shopping-cart"></i> Orders</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="/seller_reviews" target="_self"><i class="fas fa-star"></i> Reviews</a>
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
st.markdown(seller_navbar_html, unsafe_allow_html=True)

user_designation = fetch_user_designation(st.session_state.user[1])

if user_designation:
    if user_designation == 'Admin':
        st.switch_page('app.py')
    if user_designation == 'Seller':
        st.markdown(seller_navbar_html, unsafe_allow_html=True)
    if user_designation == 'Customer':
        st.switch_page('pages/user_products.py')

# /////////////////////////////////////////////////////////////////////////////////////////////////////////
st.markdown("""
<style>
	.stTabs [data-baseweb="tab-list"] {
		gap: 3rem;
    }
</style>""", unsafe_allow_html=True)

user_id = st.session_state.user[0]
orders = fetch_orders(user_id)
delivered_orders = fetch_delivered_orders(user_id)

cola, colb, colc = st.columns([0.5,10,0.5])

with colb:
    with st.container(border=True):
            if orders:
                st.header("Your Order Requests")
                st.write(" ")
                for order in orders:
                    product_id, product_category, product_name, product_brand, product_weight_g, price, order_id, order_status, address, phone, image1 = order
                    col1, col2, col3, col4, col5, col6 = st.columns([1, 3, 4, 2, 2, 2])
        
                    if image1:
                        col1.image(image1, use_column_width=True)
                    col2.write(f'{product_brand} - {product_name}({product_weight_g}g)')
                    col3.write(f'{address} - {phone}')
                    col4.write(f'{price} R$')
                    col5.write(f'**{order_status}**')

                    if order_status != 'Delivered':
                        new_order_status = col6.selectbox(
                            'Change Order Status', 
                            ['Created', 'Shipped', 'Cancelled', 'Delivered', 'Invoiced', 'Unavailable', 'Processing', 'Approved'], 
                            index=['Created', 'Shipped', 'Cancelled', 'Delivered', 'Invoiced', 'Unavailable', 'Processing', 'Approved'].index(order_status),
                            key=f'status_{order_id}'  # Unique key based on order_id
                        )
                        
                        if new_order_status != order_status:
                            update_order_status(new_order_status, order_id)
                            st.switch_page('pages/seller_orders.py')
                    
                            
                            # update_order_status(new_order_status, order_id)
                            # st.experimental_rerun()
                            # st.switch_page('pages/seller_orders.py')

                    st.markdown("""<hr style="height:1px;border:none;color:#333;background-color:#333;width:99%;" /> """, unsafe_allow_html=True)
            else:
                st.write(" ")
                st.write("You have no orders.")

        # st.markdown("""<hr style="height:1px;border:none;color:#333;background-color:#333;width:90%;" /> """, unsafe_allow_html=True)
                
                    
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