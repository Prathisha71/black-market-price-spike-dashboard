# db_reset.py
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "database", "spikealert.db")

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS commodity_prices")
cursor.execute("DROP TABLE IF EXISTS price_spikes")
conn.commit()
conn.close()

print("✅ Database reset successfully. Now run run_pipeline.py again.")
