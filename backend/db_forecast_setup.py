# db_forecast_setup.py
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "database", "spikealert.db")

def create_forecast_table():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS commodity_forecasts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            commodity TEXT,
            market TEXT,
            date TEXT,
            predicted_price REAL
        )
    """)

    conn.commit()
    conn.close()
    print("✅ Forecast table created successfully!")

if __name__ == "__main__":
    create_forecast_table()
