from fetch_prices import fetch_and_combine_data, store_in_database
from anomaly_detection import detect_spikes

def run_pipeline():
    # Fetch + combine historical + real-time data
    df = fetch_and_combine_data()

    # Store into database
    store_in_database(df)

    # Run anomaly detection
    detect_spikes()

if __name__ == "__main__":
    run_pipeline()
