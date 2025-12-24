from db_config import initialize_database
from combined_data_pipeline import run_pipeline

if __name__ == "__main__":
    initialize_database()
    run_pipeline()
    print("✅ All steps completed successfully!")
