import pandas as pd
from db_config import get_db_connection

conn = get_db_connection()
query = "SELECT commodity, market, COUNT(*) as cnt FROM commodity_prices GROUP BY commodity, market"
df = pd.read_sql_query(query, conn)
conn.close()

# Show pairs with at least 5 entries
print(df[df['cnt'] >= 5])
