# anomaly_detection.py
import pandas as pd
import sqlite3
from db_config import get_db_connection
import numpy as np

# Helper: classify spike severity

def classify_spike(spike_percent):
    if spike_percent >= 20:
        return "High"
    elif spike_percent >= 10:
        return "Medium"
    else:
        return "Low"


# Spike detection function (chunked for large data)

def detect_spikes(chunk_size=500000):
    conn = get_db_connection()
    total_rows = pd.read_sql_query("SELECT COUNT(*) as cnt FROM commodity_prices", conn)['cnt'][0]
    print(f"🔹 Starting spike detection in chunks... Total rows: {total_rows}")

    offset = 0
    spikes_list = []

    while offset < total_rows:
        query = f"""
        SELECT * FROM commodity_prices
        LIMIT {chunk_size} OFFSET {offset}
        """
        chunk = pd.read_sql_query(query, conn)

        if chunk.empty:
            break

        # Convert date to datetime
        chunk['date'] = pd.to_datetime(chunk['date'])

        # Group by commodity + market
        grouped = chunk.groupby(['commodity', 'market'])

        for (commodity, market), group in grouped:
            group = group.sort_values('date')
            prices = group['price'].values

            if len(prices) < 2:
                continue  # Need at least 2 days to detect spike

            # Compute percentage change
            old_prices = prices[:-1]
            new_prices = prices[1:]
            spike_percent = ((new_prices - old_prices) / old_prices) * 100

            for i, pct in enumerate(spike_percent):
                spikes_list.append({
                    "commodity": commodity,
                    "market": market,
                    "state": group['state'].values[i+1] if 'state' in group.columns else None,
                    "date": group['date'].values[i+1],
                    "old_price": old_prices[i],
                    "new_price": new_prices[i],
                    "spike_percent": pct,
                    "alert_level": classify_spike(pct)
                })

        offset += chunk_size
        print(f"Processed {offset}/{total_rows} rows")

    # Convert to DataFrame
    spikes_df = pd.DataFrame(spikes_list)

    # Save to database
    if not spikes_df.empty:
        spikes_df.to_sql("price_spikes", conn, if_exists="append", index=False)
        print(f"✅ Detected and stored {len(spikes_df)} spikes!")
    else:
        print("✅ No spikes detected in this run.")

    conn.close()



# Run as script

if __name__ == "__main__":
    detect_spikes()
