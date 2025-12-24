import pandas as pd
import os
from db_config import get_db_connection

# Paths
HISTORICAL_CSV_FOLDER = r"C:\Users\Prath\Documents\project\SpikeAlert-Dashboard\historical_data\Agmarknet-master"
REALTIME_CSV = r"C:\Users\Prath\Downloads\9ef84268-d588-465a-a308-a864a43d0070.csv"

# Columns we want (normalized)
EXPECTED_COLUMNS = ["state", "district", "market", "commodity", "variety", "arrival_date", "min_price", "max_price", "modal_price"]

def load_csv(file_path):
    """Load a CSV and normalize column names to lowercase with underscores"""
    df = pd.read_csv(file_path)
    df.columns = [c.strip().lower().replace(" ", "_").replace("_x0020_", "_") for c in df.columns]

    # Keep only columns that exist in this file
    columns_to_keep = [col for col in EXPECTED_COLUMNS if col in df.columns]
    df = df[columns_to_keep]

    # Rename columns for consistency
    df.rename(columns={
        "arrival_date": "date",
        "min_price": "min",
        "max_price": "max",
        "modal_price": "price"
    }, inplace=True)

    # Drop rows without essential data
    essential_cols = [col for col in ["commodity", "price"] if col in df.columns]
    df.dropna(subset=essential_cols, inplace=True)

    # Convert numeric fields safely
    for col in ["price", "min", "max"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Drop rows where price is missing
    if "price" in df.columns:
        df.dropna(subset=["price"], inplace=True)

    # Format date
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.date

    return df

def fetch_and_combine_data():
    """Load historical + real-time CSVs and combine into single DataFrame"""

    # 1️⃣ Load historical CSVs
    hist_dfs = []
    for root, dirs, files in os.walk(HISTORICAL_CSV_FOLDER):
        for file in files:
            if file.endswith(".csv"):
                file_path = os.path.join(root, file)
                try:
                    df = load_csv(file_path)
                    hist_dfs.append(df)
                except Exception as e:
                    print(f"❌ Failed to load {file}: {e}")

    historical_df = pd.concat(hist_dfs, ignore_index=True) if hist_dfs else pd.DataFrame()
    print(f"✅ Loaded historical data: {len(historical_df)} rows")

    # 2️⃣ Load real-time CSV
    try:
        realtime_df = load_csv(REALTIME_CSV)
        print(f"✅ Loaded real-time data: {len(realtime_df)} rows")
    except Exception as e:
        print(f"❌ Failed to load real-time CSV: {e}")
        realtime_df = pd.DataFrame()

    # 3️⃣ Combine
    combined_df = pd.concat([historical_df, realtime_df], ignore_index=True)
    print(f"✅ Combined data: {len(combined_df)} rows total")
    return combined_df

def store_in_database(df):
    """Insert combined data into SQLite database"""
    if df.empty:
        print("❌ No data to store")
        return

    conn = get_db_connection()
    df.to_sql("commodity_prices", conn, if_exists="append", index=False)
    conn.close()
    print(f"✅ Stored {len(df)} records in database")

def run_pipeline():
    df = fetch_and_combine_data()
    store_in_database(df)
    print("✅ Pipeline finished!")
