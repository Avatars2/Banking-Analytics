-- Ensure the analytics database is created and selected
CREATE DATABASE IF NOT EXISTS banking_analytics;
USE banking_analytics;

-- Main raw data table (already existing or created previously)
CREATE TABLE IF NOT EXISTS customer_churn (
    RowNumber INT,
    CustomerId INT PRIMARY KEY,
    Surname VARCHAR(100),
    CreditScore INT,
    Geography VARCHAR(50),
    Gender VARCHAR(20),
    Age INT,
    Tenure INT,
    Balance DECIMAL(15, 2),
    NumOfProducts INT,
    HasCrCard INT,
    IsActiveMember INT,
    EstimatedSalary DECIMAL(15, 2),
    Exited INT
);

-- Indexes for fast querying
CREATE INDEX idx_geography ON customer_churn(Geography);
CREATE INDEX idx_exited ON customer_churn(Exited);

-- New Phase 2 Table: customer_analytics
CREATE TABLE IF NOT EXISTS customer_analytics (
    CustomerId INT PRIMARY KEY,
    RFM_Score INT,
    AgeGroup VARCHAR(20),
    BalanceSegment VARCHAR(20),
    CLV_Score DECIMAL(15, 2),
    ChurnRiskFlag VARCHAR(20),
    CreditRiskBand VARCHAR(20),
    FOREIGN KEY (CustomerId) REFERENCES customer_churn(CustomerId) ON DELETE CASCADE
);