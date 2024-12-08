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

# Function to create a product
def create_product(seller_id, product_name, product_brand, product_category, 
                   product_weight_g, product_length_cm, product_width_cm, 
                   product_height_cm, product_price, product_images):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    try:
        c.execute('''
            INSERT INTO products (seller_id, product_name, product_brand, product_category,
                                  product_weight_g, product_length_cm, product_width_cm,
                                  product_height_cm, price, image1, image2, image3)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (seller_id, product_name, product_brand, product_category,
              product_weight_g, product_length_cm, product_width_cm,
              product_height_cm, product_price,
              *product_images))
        conn.commit()
        st.success('Product added successfully!')
    except sqlite3.IntegrityError:
        st.warning('Error occurred while adding the product.')
    except Exception as e:
        st.error(f'Error: {str(e)}')
    conn.close()
    st.rerun()

def get_current_seller_id():
    if 'logged_in' not in st.session_state or not st.session_state.logged_in:
        user = fetch_logged_in_user()
        if user:
            st.session_state.logged_in = True
            st.session_state.user = user
        else:
            st.session_state.logged_in = False
            st.session_state.user = None

    if st.session_state.logged_in and st.session_state.user:
        # Assuming seller ID is at index 0 of user details
        return st.session_state.user[0]
    else:
        return None

seller_id = get_current_seller_id()

def get_products(seller_id):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        SELECT product_id, seller_id, product_category, product_name, product_brand, 
               product_weight_g, product_length_cm, product_width_cm, product_height_cm, 
               price, quantity, image1, image2, image3 
        FROM products
        WHERE seller_id = ?
    ''', (seller_id,))
    products = c.fetchall()
    conn.close()
    return products


def delete_product(product_id):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('DELETE FROM products WHERE product_id = ?', (product_id,))
    conn.commit()
    conn.close()
    st.success("Product deleted successfully!")


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
admin_navbar_html = f"""
<nav class="navbar navbar-expand-lg navbar-dark fixed-top" tabindex="-1" data-testid="stHeader">
  <a class="navbar-brand" href="/app" style="padding-left: 5px;"><i class="fas fa-chart-line"></i> <b>SuperSales</b></a>

  <div class="collapse navbar-collapse" id="navbarSupportedContent">
    <ul class="navbar-nav justify-content-center mx-auto">
      <li class="nav-item">
        <a class="nav-link" href="/app" target="_self"><i class="fas fa-search"></i> Explore</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="/report" target="_self"><i class="fas fa-file-alt"></i> Reports</a>
      </li>
      <li class="nav-item">
        <a class="nav-link active" href="/products" target="_self"><i class="fas fa-shopping-bag"></i> Products</a>
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
st.markdown(admin_navbar_html, unsafe_allow_html=True)

user_designation = fetch_user_designation(st.session_state.user[1])

if user_designation:
    if user_designation == 'Admin':
        st.markdown(admin_navbar_html, unsafe_allow_html=True)

# /////////////////////////////////////////////////////////////////////////////////////////////////////////
st.markdown("""
<style>
	.stTabs [data-baseweb="tab-list"] {
		gap: 3rem;
    }
</style>""", unsafe_allow_html=True)

st.write("Changeeeeeeeeee")
# Account Information Section
tab1, tab2 = st.tabs(["View Products", "Add a new Product"])

with tab1:
    st.header("Your Products")
    st.write(" ")
    seller_id = get_current_seller_id()
    products = get_products(seller_id)
    for product in products:
        product_id, seller_id, product_category, product_name, product_brand, \
        product_weight_g, product_length_cm, product_width_cm, product_height_cm, \
        price, quantity, image1, image2, image3 = product
        
        col1, col2, col3, col4, col5, col6, col7, col8, col9, col10, col11 = st.columns([1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1])
        
        col1.write(product_name)
        col2.write(product_brand)
        col3.write(product_category)
        col4.write(f'{product_weight_g} g')
        col5.write(f'{product_length_cm} x {product_width_cm} x {product_height_cm} cm')
        col6.write(f'{price} BRL')
        col7.write(f'{quantity} pcs')
        
        if image1:
            col8.image(image1, caption='Image 1', use_column_width=True)
        if image2:
            col9.image(image2, caption='Image 2', use_column_width=True)
        if image3:
            col10.image(image3, caption='Image 3', use_column_width=True)
        
        if col11.button("Delete", key=f"delete_{product_id}"):
            with col11:
                if st.button("Confirm Deletion"):
                    delete_product(product_id)
                    st.rerun()
                if st.button("Cancel"):
                    st.rerun()
        st.markdown("""<hr style="height:1px;border:none;color:#333;background-color:#333;width:90%;" /> """, unsafe_allow_html=True)

with tab2:
    col1, col2, col3 = st.columns([2, 4, 2])
            # with tab1:
    with col2:
        with st.container(border=True):
            seller_id = get_current_seller_id()

            st.header("Add a new Product")
            product_name = st.text_input('Enter the Name of the Product', key='product_name')
            product_brand = st.text_input('Enter the Brand Name of the Product', key='product_brand')
            product_category = st.selectbox('Select product category', product_categories)
            product_weight_g = st.number_input('Weight in grams', key='product_weight_g')
            product_length_cm = st.number_input('Length in centimeters', key='product_length_cm')
            product_width_cm = st.number_input('Width in centimeters', key='product_width_cm')
            product_height_cm = st.number_input('Height in centimeters', key='product_height_cm')
            product_price = st.number_input('Price in Brazilian Real', key='product_price')

            # Up to 3 image uploaders
            product_images = []
            for i in range(3):
                uploaded_file = st.file_uploader(f'Upload image {i+1} of the product', type=['png', 'jpg'])
                if uploaded_file is not None:
                    product_images.append(uploaded_file.read())

            if st.button('Add Product', key='add_product_button'):
                if not product_name or not product_brand or not product_category:
                    st.warning('Please fill in all required fields!')
                else:
                    create_product(seller_id, product_name, product_brand, product_category,
                                product_weight_g, product_length_cm, product_width_cm,
                                product_height_cm, product_price, product_images)

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