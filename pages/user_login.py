import streamlit as st
import sqlite3
import hashlib
from pages.auth import *
import pandas as pd
import os
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

# Function to create a new user
def create_user(username, email, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    try:
        c.execute('''
            INSERT INTO users (username, email, password, state, designation) VALUES (?, ?, ?, 0, 'Customer')
                  ''', (username, email, hash_password(password)))
        conn.commit()
        st.success('Account created successfully!')
    except sqlite3.IntegrityError:
        st.warning('Username or Email already exists')
    conn.close()

# Function to validate login
def validate_login(email, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, hash_password(password)))
    user = c.fetchone()
    if user:
        c.execute('UPDATE users SET state = 1 WHERE email = ?', (email,))
        conn.commit()
    conn.close()
    return user

# Function to check if user is logged in
def check_logged_in():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE state = 1')
    user = c.fetchone()
    conn.close()
    return user

def app():

    # Custom CSS for styling
    st.markdown("""
    <style>
    .auth-form {
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .auth-header {
        text-align: center;
        margin-bottom: 30px;
    }
    .stButton>button {
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<link href='https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css' rel='stylesheet'><h1 class='auth-header'><i class='fas fa-chart-line'></i><b>SuperSales</b></h1>", unsafe_allow_html=True)

    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    user = check_logged_in()
    if user:
        st.session_state.logged_in = True
        st.session_state.username = user[1]

    if st.session_state.logged_in:
        st.write(f"Welcome, {st.session_state.username}!")
        if st.button('Logout', key='logout_button'):
            logout_user(user[2])
            st.session_state.logged_in = False
            st.session_state.username = None
            st.experimental_set_query_params(logged_in=False)
            st.rerun()
    else:
        tab1, tab2 = st.tabs(["Login", "Sign Up"])
        
        with tab1:
            st.subheader("Login to Your Account")
            email = st.text_input('Email Address', key='login_email')
            password = st.text_input('Password', type='password', key='login_password')
            if st.button('Login', key='login_button'):
                user = validate_login(email, password)
                if user:
                    st.success('Logged in successfully!')
                    st.session_state.logged_in = True
                    st.session_state.username = user[1]
                    st.experimental_set_query_params(logged_in=True)
                    user_designation = st.session_state.username = user[5]

                    if user_designation:
                        if user_designation == 'Admin':
                            st.switch_page('app.py')
                        if user_designation == 'Seller':
                            st.switch_page('pages/seller_dashboard.py')
                            st.markdown(seller_navbar_html, unsafe_allow_html=True)
                        if user_designation == 'Customer':
                            st.switch_page('pages/user_products.py')

                else:
                    st.error('Login Failed: Invalid email or password')

        with tab2:
            st.subheader("Create a New Account")
            username = st.text_input('Enter your username', key='signup_username')
            email = st.text_input('Email Address', key='signup_email')
            password = st.text_input('Password', type='password', key='signup_password')
            # residing_state = st.selectbox('Select your State', customer_states)

            if st.button('Create account', key='signup_button'):
                if len(password) < 6:
                    st.warning('Password must be at least 6 characters long')
                elif '@' not in email:
                    st.warning('Invalid email address')
                elif not username:
                    st.warning('Username cannot be empty')
                # elif not residing_state:
                #     st.warning('Please select a state')
                else:
                    create_user(username, email, password)

if __name__ == "__main__":
    app()
