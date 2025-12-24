import pandas as pd
from db_config import get_db_connection
from statsmodels.tsa.arima.model import ARIMA
import warnings

warnings.filterwarnings("ignore")

def forecast_prices(commodity_name, market_name, steps=7):
    """Generate ARIMA forecast for a given commodity + market."""
    
    conn = get_db_connection()
    query = f"""
        SELECT date, price 
        FROM commodity_prices 
        WHERE commodity='{commodity_name}' AND market='{market_name}' 
        ORDER BY date
    """
    df = pd.read_sql_query(query, conn)
    conn.close()

    if df.empty or len(df) < 5:
        print(f"❌ Not enough data to forecast for {commodity_name} in {market_name}")
        return None

    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)

    try:
        model = ARIMA(df['price'], order=(1,1,1))
        model_fit = model.fit()
        forecast = model_fit.forecast(steps=steps)

        forecast_df = pd.DataFrame({
            'commodity': commodity_name,
            'market': market_name,
            'date': pd.date_range(start=df.index[-1] + pd.Timedelta(days=1), periods=steps),
            'predicted_price': forecast.values
        })

        print(f"✅ Forecast generated for {commodity_name} in {market_name}")
        return forecast_df

    except Exception as e:
        print("❌ Forecasting failed:", e)
        return None

def store_forecast_in_db(forecast_df):
    """Store forecasted prices into the commodity_forecasts table."""
    if forecast_df is None or forecast_df.empty:
        return

    conn = get_db_connection()
    forecast_df.to_sql("commodity_forecasts", conn, if_exists="append", index=False)
    conn.close()
    print(f"✅ Stored {len(forecast_df)} forecasted rows into database")

if __name__ == "__main__":
    # Example: Forecast next 7 days for all available commodity + market pairs
    conn = get_db_connection()
    pairs = pd.read_sql_query("SELECT DISTINCT commodity, market FROM commodity_prices", conn)
    conn.close()

    for _, row in pairs.iterrows():
        commodity = row['commodity']
        market = row['market']
        forecast_df = forecast_prices(commodity, market, steps=7)
        store_forecast_in_db(forecast_df)
