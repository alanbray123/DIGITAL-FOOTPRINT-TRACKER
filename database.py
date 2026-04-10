import sqlite3

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "activity.db")

def connect():
    return sqlite3.connect(DB_NAME)

def create_table():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        activity TEXT,
        timestamp TEXT
    )
    """)

    conn.commit()
    conn.close()

def insert_log(activity, timestamp):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO logs (activity, timestamp) VALUES (?, ?)",
                   (activity, timestamp))

    conn.commit()
    conn.close()

def fetch_logs():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM logs ORDER BY timestamp DESC LIMIT 50")
    data = cursor.fetchall()

    conn.close()
    return data