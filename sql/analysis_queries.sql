-- ====================================================================
-- Phase 2: Analytical & BI Reporting Queries
-- ====================================================================

-- Query 1: Customer Segmentation Counts by Balance Segment and Geography
SELECT 
    c.Geography,
    a.BalanceSegment,
    COUNT(c.CustomerId) AS Total_Customers
FROM customer_churn c
JOIN customer_analytics a ON c.CustomerId = a.CustomerId
GROUP BY c.Geography, a.BalanceSegment
ORDER BY c.Geography, Total_Customers DESC;

-- Query 2: Average CLV Score by Age Group
SELECT 
    a.AgeGroup,
    ROUND(AVG(a.CLV_Score), 2) AS Avg_CLV_Score,
    COUNT(a.CustomerId) AS Customer_Count
FROM customer_analytics a
GROUP BY a.AgeGroup
ORDER BY Avg_CLV_Score DESC;

-- Query 3: Credit Risk & Churn Rate by Credit Risk Band
SELECT 
    a.CreditRiskBand,
    COUNT(*) AS Total_Customers,
    SUM(c.Exited) AS Total_Churned,
    ROUND((SUM(c.Exited) / COUNT(*)) * 100, 2) AS Churn_Rate_Pct
FROM customer_churn c
JOIN customer_analytics a ON c.CustomerId = a.CustomerId
GROUP BY a.CreditRiskBand
ORDER BY Churn_Rate_Pct DESC;

-- Query 4: Top 10 Highest-Value At-Risk Customers
SELECT 
    c.CustomerId,
    c.Surname,
    c.Geography,
    c.Balance,
    a.CLV_Score
FROM customer_churn c
JOIN customer_analytics a ON c.CustomerId = a.CustomerId
WHERE a.ChurnRiskFlag = 'High Risk'
ORDER BY a.CLV_Score DESC
LIMIT 10;

-- Query 5: Average RFM Score and Churn Rate by Geography
SELECT 
    c.Geography,
    ROUND(AVG(a.RFM_Score), 2) AS Avg_RFM_Score,
    ROUND(AVG(c.Exited) * 100, 2) AS Churn_Rate_Pct
FROM customer_churn c
JOIN customer_analytics a ON c.CustomerId = a.CustomerId
GROUP BY c.Geography
ORDER BY Avg_RFM_Score DESC;