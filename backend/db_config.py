import sqlite3
import os

# Define path to your database file
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "database", "spikealert.db")

def get_db_connection():
    """Return a connection to the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    return conn

def initialize_database():
    """Create tables if they don't exist."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Table for storing commodity prices
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS commodity_prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            state TEXT,
            district TEXT,
            market TEXT,
            commodity TEXT,
            variety TEXT,
            date TEXT,
            min REAL,
            max REAL,
            price REAL
        )
    """)

    # Table for storing anomaly alerts
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS price_spikes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            commodity TEXT,
            market TEXT,
            date TEXT,
            old_price REAL,
            new_price REAL,
            spike_percent REAL,
            alert_level TEXT
        )
    """)

    conn.commit()
    conn.close()
    print("✅ Database initialized successfully!")

if __name__ == "__main__":
    initialize_database()
