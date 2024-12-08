import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import plotly.express as px

st.set_page_config(
    page_title="SuperSales - Reviews",
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


# Define the navbar HTML with updated styles and Font Awesome icons
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
        <a class="nav-link active" href="/review" target="_self"><i class="fas fa-star"></i> Reviews</a>
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
        <a class="nav-link active" href="/review" target="_self"><i class="fas fa-star"></i> Reviews</a>
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
if st.session_state.user[1] == 'Admin':
    st.markdown(admin_navbar_html, unsafe_allow_html=True)
else:
    st.markdown(user_navbar_html, unsafe_allow_html=True)


# ///////////////////////////////////////////////////////////////////////////////////////////////////

# Function to load data and cache it
@st.cache_data  # Cache the returned dataframe
def load_data(file_path):
    return pd.read_csv(file_path)

# Get the directory of the current script
current_dir = os.path.dirname('app.py')
file_path = os.path.join(current_dir, 'Data/New/orders_all.csv')
# Load the properties data
df = load_data(file_path)

# ////////////////////////////////////////////////////////////////////////////////////////////////
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
        font-size: 1.5em;
        color: #808080;
        text-align: center;
        margin-top: 0;
    }
    hr {
        border: none;
        height: 2px;
        background-color: grey;
        margin: 10px 0;
    }
    .h-title {
        font-size: 1.4em;
        font-weight: bold;
        color: white;
        text-align: center;
        margin-bottom: 15px;
        background-color: #787878;
        border-radius: 10px;
        padding: 3px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Dashboard title and subtitle
st.markdown('<div class="header-title">Review Sentiment Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="header-subtitle">Analyzing the sentiments of product reviews</div>', unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# Function to load data and cache it
@st.cache_data  # Cache the returned dataframe
def load_data(file_path):
    return pd.read_csv(file_path)

# Get the directory of the current script
current_dir = os.path.dirname('app.py')
file_path = os.path.join(current_dir, 'Data/New/orders_all.csv')
# Load the properties data
df = load_data(file_path)

# //////////////////////////////////////////////////////////////////////////////////////

import altair as alt

# Preprocess data
df['sibert_result'] = df['sibert_result'].fillna('Not Reviewed')
df['sibert_result'] = df['sibert_result'].replace({'POSITIVE': 'Positive', 'NEGATIVE': 'Negative'})
color_palette = ['#7defa1', '#83c9ff', '#976de3']

# Create a multi-select dropdown with checkboxes for product categories
selected_categories = st.multiselect("Select categories to filter:", df['product_category'].unique(), default=df['product_category'].unique())

# Filter data based on selected categories
filtered_df = df[df['product_category'].isin(selected_categories)]


col1, col2 = st.columns(2)
with col1:
    with st.container(border=True):
        st.markdown('<div class="h-title">Overall Reviews</div>', unsafe_allow_html=True)
        review_counts = filtered_df['sibert_result'].value_counts().reset_index()
        review_counts.columns = ['Sentiment', 'Count']

        # Create the bar chart
        bar_chart = alt.Chart(review_counts).mark_bar().encode(
            x='Sentiment',
            y='Count',
            color=alt.Color('Sentiment', legend=None, scale=alt.Scale(domain=review_counts['Sentiment'].unique(), range=color_palette)),
            tooltip=['Sentiment', 'Count']  # Custom tooltip
        ).properties(
            height=520,  # Set height to 500 pixels
            title="Sentiment Distribution of Reviews"
        ).interactive()

        # Display the chart
        st.altair_chart(bar_chart, theme="streamlit", use_container_width=True)
        
        # Adding textual insights
        total_reviews = len(filtered_df)
        positive_reviews = review_counts[review_counts['Sentiment'] == 'Positive']['Count'].values[0]
        negative_reviews = review_counts[review_counts['Sentiment'] == 'Negative']['Count'].values[0]
        not_reviewed = review_counts[review_counts['Sentiment'] == 'Not Reviewed']['Count'].values[0]
        
        st.write(f"Out of {total_reviews} reviews, {positive_reviews} are positive, {negative_reviews} are negative, and {not_reviewed} are not reviewed.")

with col2:
    with st.container(border=True):
        st.markdown('<div class="h-title">Detailed Sentiment Analysis</div>', unsafe_allow_html=True)
        cola, colb = st.columns([2, 1])
        with cola:
            # Create a dropdown menu for sentiment selection
            selected_sentiment = st.selectbox("Select a sentiment to view details:", review_counts['Sentiment'])

        if selected_sentiment:
            count = review_counts[review_counts['Sentiment'] == selected_sentiment]['Count'].values[0]
            percentage = (count / len(filtered_df)) * 100
            st.write(f"You selected {selected_sentiment} reviews ({count} reviews, {percentage:.2f}%)")

            # Show some insight based on the selected sentiment
            st.write(f"**Percentage of {selected_sentiment} reviews per category**")
            category_counts = filtered_df[filtered_df['sibert_result'] == selected_sentiment]['product_category'].value_counts(normalize=True) * 100
            category_counts = category_counts.reset_index()
            category_counts.columns = ['Product Category', 'Proportion']
            category_counts['Proportion'] = round(category_counts['Proportion'], 3)

            # Create the pie chart with custom tooltip
            pie_chart = alt.Chart(category_counts).mark_arc(innerRadius=70, outerRadius=160).encode(
                theta='Proportion',
                color='Product Category',
                tooltip=['Product Category', 'Proportion']  # Custom tooltip
            ).interactive()

            # Display the chart
            st.altair_chart(pie_chart, use_container_width=True)
            
            count = review_counts[review_counts['Sentiment'] == selected_sentiment]['Count'].values[0]
            percentage = (count / len(filtered_df)) * 100
            st.write(f"You selected {selected_sentiment} reviews ({count} reviews, {percentage:.2f}%)")

            # Show some insight based on the selected sentiment
            st.write(f"**Percentage of {selected_sentiment} reviews per category**")
            category_counts = filtered_df[filtered_df['sibert_result'] == selected_sentiment]['product_category'].value_counts(normalize=True) * 100
            category_counts = category_counts.reset_index()
            category_counts.columns = ['Product Category', 'Proportion']
            category_counts['Proportion'] = round(category_counts['Proportion'], 3)

            # Create a formatted list of categories and proportions
            insights_list = "\n".join([f"- **{row['Product Category']}**: {row['Proportion']}%" for index, row in category_counts.iterrows()])

            # Display the insights in a markdown format
            st.markdown(insights_list)

          # # Example of adding more insights
          # if selected_sentiment == 'Positive':
          #     st.write("Positive reviews are highest in Electronics and Groceries.")
          # elif selected_sentiment == 'Negative':
          #     st.write("Negative reviews are predominantly in Clothing.")
          # else:
          #     st.write("Not Reviewed category shows an even distribution across different product categories.")

        # # Example of adding more insights
        # if selected_sentiment == 'Positive':
        #     st.write("Positive reviews are highest in Electronics and Groceries.")
        # elif selected_sentiment == 'Negative':
        #     st.write("Negative reviews are predominantly in Clothing.")
        # else:
        #     st.write("Not Reviewed category shows an even distribution across different product categories.")
# //////////////////////////////////////////////////////////////////////////////////////

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