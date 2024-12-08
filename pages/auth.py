import sqlite3
import hashlib

# Function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

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

# Function to log out the user
def logout_user(email):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('UPDATE users SET state = 0 WHERE email = ?', (email,))
    conn.commit()
    conn.close()
