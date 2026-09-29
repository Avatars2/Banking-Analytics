"""
Loads Churn_Modelling.csv into the `customer_churn` table in MySQL.

Setup:
    1. Copy .env.example (in project root) to .env
    2. Fill in your real DB credentials in .env
    3. pip install -r requirements.txt
    4. Run: python scripts/upload.py
"""

import os
import pandas as pd
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

load_dotenv()  # reads variables from .env into the environment

CSV_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "raw", "Churn_Modelling.csv")

# 1. Read the Kaggle CSV
print(f"Reading data from {CSV_FILE}...")
df = pd.read_csv(CSV_FILE)

# 2. Establish MySQL Connection (credentials come from environment, not hardcoded)
try:
    connection = mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME", "banking_analytics"),
    )

    if connection.is_connected():
        cursor = connection.cursor()
        print("Connected to MySQL database successfully.")

        # 3. Prepare the Insert Query
        insert_query = """
        INSERT INTO customer_churn (
            RowNumber, CustomerId, Surname, CreditScore, Geography,
            Gender, Age, Tenure, Balance, NumOfProducts,
            HasCrCard, IsActiveMember, EstimatedSalary, Exited
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        # 4. Insert data line-by-line
        print(f"Uploading {len(df)} rows to MySQL...")
        for index, row in df.iterrows():
            cursor.execute(insert_query, tuple(row))

        connection.commit()
        print(f"Success! All {len(df)} rows uploaded to table 'customer_churn'.")

except Error as e:
    print(f"Error while connecting to MySQL: {e}")

finally:
    if "connection" in locals() and connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection closed securely.")
