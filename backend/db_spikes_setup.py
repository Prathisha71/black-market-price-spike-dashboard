# db_spikes_setup.py
import sqlite3
from db_config import DB_PATH  # make sure you have DB_PATH in db_config.py

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Drop old table if exists
cursor.execute("DROP TABLE IF EXISTS price_spikes")

# Create new table with all required columns
cursor.execute("""
CREATE TABLE price_spikes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    commodity TEXT NOT NULL,
    market TEXT NOT NULL,
    state TEXT,
    date TEXT NOT NULL,
    old_price REAL,
    new_price REAL,
    spike_percent REAL,
    alert_level TEXT
)
""")

conn.commit()
conn.close()
print("✅ price_spikes table created successfully with all columns!")
