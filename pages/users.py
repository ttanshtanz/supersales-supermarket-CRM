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

# def create_user(username, email, password):
#     conn = sqlite3.connect('users.db')
#     c = conn.cursor()
#     try:
#         c.execute('INSERT INTO users (username, email, password, state) VALUES (?, ?, ?, 0)', (username, email, hash_password(password)))
#         conn.commit()
#         st.success('Account created successfully!')
#     except sqlite3.IntegrityError:
#         st.warning('Username or Email already exists')
#     conn.close()

def create_user(username, email, password, residing_state):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    try:
        c.execute('''
            INSERT INTO users (username, email, password, state, designation, residing_state) VALUES (?, ?, ?, 0, 'Seller', ?)
                  ''', (username, email, hash_password(password), residing_state))
        conn.commit()
        st.success('Account created successfully!')
    except sqlite3.IntegrityError:
        st.warning('Username or Email already exists')
    conn.close()
    st.rerun()

def get_users():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT id, username, email, residing_state FROM users WHERE username != "Admin" and designation="Seller"')
    users = c.fetchall()
    conn.close()
    return users

def get_customers():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT id, username, email, residing_state FROM users WHERE username != "Admin" and designation="Customer"')
    users = c.fetchall()
    conn.close()
    return users

def delete_user(user_id):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('DELETE FROM users WHERE id = ?', (user_id,))
    conn.commit()
    conn.close()
    st.success('User deleted successfully')

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
        <a class="nav-link" href="/predict" target="_self"><i class="fas fa-chart-bar"></i> Predict</a>
      </li>
      <li class="nav-item">
        <a class="nav-link active" href="/chat" target="_self"><i class="fas fa-comments"></i> Chat</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="/review" target="_self"><i class="fas fa-star"></i> Reviews</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="/report" target="_self"><i class="fas fa-file-alt"></i> Reports</a>
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
if st.session_state.user[1] == 'Admin':
    st.markdown(admin_navbar_html, unsafe_allow_html=True)
else:
    st.switch_page('app.py')


# /////////////////////////////////////////////////////////////////////////////////////////////////////////
st.markdown("""
<style>
	.stTabs [data-baseweb="tab-list"] {
		gap: 3rem;
    }
</style>""", unsafe_allow_html=True)

# Account Information Section
tab1, tab2, tab3 = st.tabs(["View Sellers", "View Customers", "Add a new Seller"])

with tab1:
    st.header("Sellers")
    st.write(" ")
    users = get_users()
    for user in users:
        user_id, username, email, residing_state = user
        col1, col2, col3, col4, col5, col6 = st.columns([1, 2, 2, 2, 1, 1])
        col1.write(username)
        col2.write(email)
        col3.write(residing_state)
        if col4.button("Delete", key=f"delete_{user_id}"):
            with col5:
                if st.button("Confirm Deletion"):
                    delete_user(user_id)
                    st.rerun()
            with col6:
                if st.button("Cancel"):
                    st.rerun()
        st.markdown("""<hr style="height:1px;border:none;color:#333;background-color:#333;width:90%;" /> """, unsafe_allow_html=True)

with tab2:
    st.header("Customers")
    st.write(" ")
    users = get_customers()
    for user in users:
        user_id, username, email, residing_state = user
        col1, col2, col3, col4, col5, col6 = st.columns([1, 2, 2, 2, 1, 1])
        col1.write(username)
        col2.write(email)
        col3.write(residing_state)
        if col4.button("Delete", key=f"delete_cus_{user_id}"):
            with col5:
                if st.button("Confirm Deletion"):
                    delete_user(user_id)
                    st.rerun()
            with col6:
                if st.button("Cancel"):
                    st.rerun()
        st.markdown("""<hr style="height:1px;border:none;color:#333;background-color:#333;width:90%;" /> """, unsafe_allow_html=True)

with tab3:
    # st.header("Create a New Seller Account")
    # username = st.text_input('Enter the username', key='signup_username')
    # email = st.text_input('Email Address', key='signup_email')
    # password = st.text_input('Password', type='password', key='signup_password')

    # if st.button('Create account', key='signup_button'):
    #     if len(password) < 6:
    #         st.warning('Password must be at least 6 characters long')
    #     elif '@' not in email:
    #         st.warning('Invalid email address')
    #     elif not username:
    #         st.warning('Username cannot be empty')
    #     else:
    #         create_user(username, email, password)
    col1, col2, col3 = st.columns([2, 4, 2])
            # with tab1:
    with col2:
        with st.container(border=True):
            st.header("Create a New Seller Account")

            username = st.text_input('Enter the username', key='signup_username')
            email = st.text_input('Email Address', key='signup_email')
            password = st.text_input('Password', type='password', key='signup_password')
            residing_state = st.selectbox('Select State of Seller', customer_states)

            if st.button('Create account', key='signup_button'):
                if len(password) < 6:
                    st.warning('Password must be at least 6 characters long')
                elif '@' not in email:
                    st.warning('Invalid email address')
                elif not username:
                    st.warning('Username cannot be empty')
                elif not residing_state:
                    st.warning('Please select a state')
                else:
                    create_user(username, email, password, residing_state)

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