import os
import mysql.connector
import pandas as pd
from dotenv import load_dotenv

# 1. Load environment variables (.env)
load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "banking_analytics")

# 2. Read processed data
csv_path = os.path.join("data", "processed", "bank_analytics_ready.csv")
print(f"Reading processed data from {csv_path}...")
df = pd.read_csv(csv_path)

# Convert dataframe to tuples for executemany
records = df[
    [
        "CustomerId",
        "RFM_Score",
        "AgeGroup",
        "BalanceSegment",
        "CLV_Score",
        "ChurnRiskFlag",
        "CreditRiskBand",
    ]
].to_records(index=False)

data_to_insert = [tuple(x) for x in records]

# 3. Connect to MySQL and upload
try:
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
    )
    cursor = conn.cursor()

    insert_query = """
    INSERT INTO customer_analytics 
    (CustomerId, RFM_Score, AgeGroup, BalanceSegment, CLV_Score, ChurnRiskFlag, CreditRiskBand)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
        RFM_Score = VALUES(RFM_Score),
        AgeGroup = VALUES(AgeGroup),
        BalanceSegment = VALUES(BalanceSegment),
        CLV_Score = VALUES(CLV_Score),
        ChurnRiskFlag = VALUES(ChurnRiskFlag),
        CreditRiskBand = VALUES(CreditRiskBand)
    """

    print("Bulk inserting data into MySQL using executemany()...")
    cursor.executemany(insert_query, data_to_insert)
    conn.commit()

    print(
        f"[SUCCESS] {len(data_to_insert)} records processed in customer_analytics table!"
    )

except mysql.connector.Error as err:
    print(f"[ERROR] MySQL Error: {err}")
finally:
    if "conn" in locals() and conn.is_connected():
        cursor.close()
        conn.close()
        print("MySQL connection closed.")

