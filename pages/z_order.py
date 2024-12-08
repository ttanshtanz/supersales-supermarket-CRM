import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import plotly.express as px

st.set_page_config(
    page_title="SuperSales - Report",
    page_icon="💹",
    layout="wide",
    initial_sidebar_state="collapsed",
)

import sqlite3
# Function to fetch logged-in user's information
def fetch_logged_in_user():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE state = 1')
    user = c.fetchone()
    conn.close()
    return user

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

st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">', unsafe_allow_html=True)
st.markdown('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">', unsafe_allow_html=True)

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
    </style>
    """,
    unsafe_allow_html=True
)


# Function to load data and cache it
@st.cache_data  # Cache the returned dataframe
def load_data(file_path):
    return pd.read_csv(file_path)


# Define the navigation bar using HTML/CSS
navbar_html = """
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css" rel="stylesheet">

<style>
    .navbar {
        background-color: #00114a;
        color: white;
        z-index: 1000;
        padding: 0.5rem 1rem;
    }
    .navbar-brand {
        font-size: 1.2em;
        font-weight: bold;
        color: white !important;
    }
    .navbar-nav .nav-link {
        font-size: 1em;
        margin-left: 15px;
        margin-right: 15px;
        color: white !important;
        transition: color 0.3s ease-in-out, background-color 0.3s ease-in-out;
    }
    .navbar-nav .nav-link:hover {
        color: #cecece !important;
        background-color: rgba(255, 255, 255, 0.2);
        border-radius: 5px;
    }
    .navbar-nav .nav-link.active {
        font-weight: bold;
        background-color: rgba(255, 255, 255, 0.3);
        border-radius: 5px;
    }
    .navbar-toggler {
        border-color: rgba(255, 255, 255, 0.1);
    }
    .navbar-toggler-icon {
        background-image: url("data:image/svg+xml;charset=utf8,%3Csvg viewBox='0 0 30 30' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath stroke='rgba%2872, 118, 255, 1%29' stroke-width='2' linecap='round' linejoin='round' d='M4 7h22M4 15h22M4 23h22'/%3E%3C/svg%3E");
    }
    .navbar-nav {
        flex-direction: row;
        flex-grow: 1;
        justify-content: center;
    }
</style>

"""
st.markdown(navbar_html, unsafe_allow_html=True)

user_navbar_html="""
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
        <a class="nav-link" href="/chat" target="_self"><i class="fas fa-comments"></i> Chat</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="/review" target="_self"><i class="fas fa-star"></i> Reviews</a>
      </li>
      <li class="nav-item">
        <a class="nav-link active" href="/report" target="_self"><i class="fas fa-file-alt"></i> Reports</a>
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
        <a class="nav-link" href="/chat" target="_self"><i class="fas fa-comments"></i> Chat</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="/review" target="_self"><i class="fas fa-star"></i> Reviews</a>
      </li>
      <li class="nav-item">
        <a class="nav-link active" href="/report" target="_self"><i class="fas fa-file-alt"></i> Reports</a>
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
if st.session_state.user[1] == 'Admin':
    st.markdown(admin_navbar_html, unsafe_allow_html=True)
else:
    st.markdown(user_navbar_html, unsafe_allow_html=True)

# ////////////////////////////////////////////////////////////////////////////////////////////////

# st.title("Dashboard")

# Function to load data and cache it
@st.cache_data  # Cache the returned dataframe
def load_data(file_path):
    return pd.read_csv(file_path)

# Get the directory of the current script
current_dir = os.path.dirname('app.py')
file_path = os.path.join(current_dir, 'Data/New/all_details.csv')
# Load the properties data
df = load_data(file_path)

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
st.markdown(
    """
    <style>
    .header-title {
        font-size: 2.5em;
        font-weight: bold;
        color: white;
        text-align: center;
        margin-bottom: 0;
    }
    .header-subtitle {
        font-size: 2em;
        color: #83a5d9;
        text-align: left;
        margin-top: 0;
        font-weight:bold; 
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Dashboard title and subtitle
st.markdown('<div class="header-title">Order Status Analysis</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

import plotly.express as px
import plotly.graph_objects as go

# Convert date columns to datetime
date_columns = [
    'order_purchase_timestamp', 'order_delivered_carrier_date',
    'order_delivered_customer_date', 'order_estimated_delivery_date',
    'shipping_limit_date', 'review_answer_timestamp'
]
for col in date_columns:
    df[col] = pd.to_datetime(df[col], errors='coerce')

# Get unique product categories
product_categories = df['order_status'].unique()
product_categories = [status.capitalize() for status in product_categories]

# Create a dropdown for selecting a product category
selected_category = st.selectbox('Select Order Status', product_categories)
# Filter the DataFrame based on the selected product category
filtered_df = df[df['order_status'] == selected_category.lower()]

# Drop the order_status column from the filtered data for display
display_df = filtered_df.drop(columns=['order_status'])
total_price = filtered_df['price'].sum()
total_price_all = df['price'].sum()

# Main content
st.markdown(f'<div class="header-subtitle">Insights for {selected_category} products</div>', unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# Display insights
cola, colb = st.columns(2)
with cola:
    st.markdown(f"""
    <div class="md-6" style="background-color: rgb(213 213 213 / 57%); padding: 10px; border-radius: 5px; display:flex; margin-bottom: 10px;">
            <h4><b>Number of products</b></h4><h4 style="color: #0c0c7a;"><b>{filtered_df.shape[0]} / {df.shape[0]}</b></h4>
    </div>
    """, unsafe_allow_html=True)

with colb:
    st.markdown(f"""
    <div class="md-6" style="background-color: rgb(213 213 213 / 57%); padding: 10px; border-radius: 5px; display:flex; margin-bottom: 10px;">
           <h4><b>Total Sales</b></h4><h4 style="color: #0c0c7a;"><b>R$ {total_price:,.2f} / R$ {total_price_all:,.2f}</b></h4>
    </div>
    """, unsafe_allow_html=True)

# Display the filtered DataFrame without the order_status column
st.write("#### Filtered Data")
st.dataframe(display_df, height=300)

# Example: Generate some graphs using Plotly
st.write("#### Graphs for the Selected Category")

col1, col2, col3 = st.columns(3)

with col1:
    # Price distribution
    fig = px.histogram(filtered_df, x='price', nbins=20, title='Sales Distribution',
                       color_discrete_sequence=['#636EFA'])
    fig.update_layout(xaxis_title='Price', yaxis_title='Frequency', template='plotly_white')
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Order status counts
    order_status_counts = filtered_df['payment_type'].value_counts().reset_index()
    order_status_counts.columns = ['payment_type', 'count']
    fig = px.bar(order_status_counts, x='payment_type', y='count', title='Payment Method Counts',
                 color_discrete_sequence=['#EF553B'])
    fig.update_layout(xaxis_title='Payment Method', yaxis_title='Count', template='plotly_white')
    st.plotly_chart(fig, use_container_width=True)

with col3:
    # Review score distribution
    fig = px.histogram(filtered_df, x='review_score', nbins=5, title='Review Score Distribution',
                       color_discrete_sequence=['#00CC96'])
    fig.update_layout(xaxis_title='Review Score', yaxis_title='Frequency', template='plotly_white')
    st.plotly_chart(fig, use_container_width=True)
    
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

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