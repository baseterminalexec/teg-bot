import sqlite3
from datetime import datetime, timedelta

DB_NAME = "subscriptions.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            subscription_end TEXT
        )
    """)
    conn.commit()
    conn.close()

def add_subscription(user_id, username, duration="monthly"):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    if duration == "yearly":
        expiry_date = (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d")
    else:
        expiry_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
    
    cursor.execute("REPLACE INTO users (user_id, username, subscription_end) VALUES (?, ?, ?)", 
                   (user_id, username, expiry_date))
    conn.commit()
    conn.close()

def check_subscription(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT subscription_end FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    if result:
        expiry_date = datetime.strptime(result[0], "%Y-%m-%d")
        return expiry_date >= datetime.now()
    return False
