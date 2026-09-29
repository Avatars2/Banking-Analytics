import os
import numpy as np
import pandas as pd

# -------------------------------------------------------------------
# 1. Load Data & Quality Checks
# -------------------------------------------------------------------
raw_path = os.path.join("data", "raw", "Churn_Modelling.csv")
print(f"Loading data from: {raw_path}")
df = pd.read_csv(raw_path)

print("\n--- Data Quality Assessment ---")
print(f"Dataset Shape: {df.shape}")
print("\nNull Values Check:")
print(df.isnull().sum())

print(
    f"\nDuplicate CustomerId Count: {df.duplicated(subset=['CustomerId']).sum()}"
)
df = df.drop_duplicates(subset=["CustomerId"])

# -------------------------------------------------------------------
# 2. RFM Score Construction (Proxy Adaptation)
# -------------------------------------------------------------------
# Recency: Tenure (years with bank)
# Frequency: NumOfProducts (number of products used)
# Monetary: Balance + EstimatedSalary (total customer financial value)

df["R_Score"] = pd.qcut(
    df["Tenure"], q=5, labels=[1, 2, 3, 4, 5], duplicates="drop"
).astype(int)
df["F_Score"] = pd.qcut(
    df["NumOfProducts"].rank(method="first"),
    q=5,
    labels=[1, 2, 3, 4, 5],
    duplicates="drop",
).astype(int)
df["M_Score"] = pd.qcut(
    df["Balance"] + df["EstimatedSalary"],
    q=5,
    labels=[1, 2, 3, 4, 5],
    duplicates="drop",
).astype(int)

df["RFM_Score"] = df["R_Score"] + df["F_Score"] + df["M_Score"]

# -------------------------------------------------------------------
# 3. Feature Engineering (New Segment Columns)
# -------------------------------------------------------------------

# Feature 1: AgeGroup
age_bins = [17, 30, 45, 60, 100]
age_labels = ["18-30", "31-45", "46-60", "60+"]
df["AgeGroup"] = pd.cut(df["Age"], bins=age_bins, labels=age_labels)

# Feature 2: BalanceSegment
balance_bins = [-1, 0, 50000, 120000, np.inf]
balance_labels = ["Zero", "Low", "Medium", "High"]
df["BalanceSegment"] = pd.cut(
    df["Balance"], bins=balance_bins, labels=balance_labels
)

# Feature 3: CLV_Score (Proxy Customer Lifetime Value)
# Formula: Balance * Tenure * NumOfProducts / 100
df["CLV_Score"] = (
    df["Balance"] * df["Tenure"] * df["NumOfProducts"]
) / 100.0

# Feature 4: ChurnRiskFlag (Rule-based risk classification)
risk_condition = (
    (df["IsActiveMember"] == 0)
    & (df["Age"] > 40)
    & (df["NumOfProducts"] == 1)
)
df["ChurnRiskFlag"] = np.where(risk_condition, "High Risk", "Normal")

# Feature 5: CreditRiskBand (Standard FICO-like cutoffs)
credit_bins = [0, 579, 669, 739, 799, 850]
credit_labels = ["Poor", "Fair", "Good", "Very Good", "Exceptional"]
df["CreditRiskBand"] = pd.cut(
    df["CreditScore"], bins=credit_bins, labels=credit_labels
)

# -------------------------------------------------------------------
# 4. Save Output Data
# -------------------------------------------------------------------
output_dir = os.path.join("data", "processed")
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "bank_analytics_ready.csv")

df.to_csv(output_path, index=False)
print(f"\n[SUCCESS] Saved updated dataset to: {output_path}")

# -------------------------------------------------------------------
# 5. Output Summary Statistics for Internship Report
# -------------------------------------------------------------------
print("\n" + "=" * 50)
print("             EVIDENCE & SUMMARY REPORT")
print("=" * 50)

print("\n--- Age Group Breakdown ---")
print(df["AgeGroup"].value_counts())

print("\n--- Balance Segment Breakdown ---")
print(df["BalanceSegment"].value_counts())

print("\n--- Churn Risk Flag Breakdown ---")
print(df["ChurnRiskFlag"].value_counts())

print("\n--- Credit Risk Band Breakdown ---")
print(df["CreditRiskBand"].value_counts())

print("\n--- Numerical Summary for RFM_Score & CLV_Score ---")
print(df[["RFM_Score", "CLV_Score"]].describe())