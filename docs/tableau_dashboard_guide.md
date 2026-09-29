# Tableau Dashboard Layout Guide

This guide summarizes the expected worksheet and dashboard layout for the two Tableau workbooks in the repository.

## Customer Insights Dashboard (`Customer_Insights_Dashboard.twb`)

Purpose: Combine segmentation and CLV analysis to help business users understand customer distribution and value across geography and balance segments.

Expected layout and worksheet contents:
- Worksheet: Geographic Distribution
  - Visualize customer counts by `Geography`.
  - Use color or size to highlight differences across regions.
- Worksheet: Balance Segment Breakdown
  - Show counts or percentages by `BalanceSegment`.
  - Optional cross-filter by `Geography` for deeper segmentation.
- Worksheet: Age Group Analysis
  - Display customer counts across `AgeGroup` categories (18-30, 31-45, 46-60, 60+).
  - Include churn counts or rate if available.
- Worksheet: Average CLV by Segment
  - Present average `CLV_Score` grouped by `BalanceSegment`, `AgeGroup`, or `Geography`.
  - Use bars or heatmap-style marks to call out high-value segments.
- Filters and interactivity:
  - Global dashboard filters for `Geography` and `BalanceSegment`.
  - If possible, add `AgeGroup` as a quick filter for drill-downs.

Data source reference:
- Should connect to `data/processed/bank_analytics_ready.csv`.
- Ensure engineered fields are available: `RFM_Score`, `AgeGroup`, `BalanceSegment`, `CLV_Score`, `ChurnRiskFlag`, `CreditRiskBand`.

## Risk Assessment Dashboard (`Risk_Assessment_Dashboard.twb`)

Purpose: Combine churn and financial risk views to identify at-risk customers and support risk mitigation strategies.

Expected layout and worksheet contents:
- Worksheet: Churn Rate by Credit Risk Band
  - Visualize churn rate or churn count grouped by `CreditRiskBand`.
  - Include total customer count per band and churn rate percentage.
- Worksheet: High Risk Customer Flags
  - Highlight customers or segments where `ChurnRiskFlag = 'High Risk'`.
  - Show distribution of those customers by `Geography` or `CreditRiskBand`.
- Worksheet: Balance Risk Matrix
  - Show `Balance` distribution against `CLV_Score`, `CreditRiskBand`, or `ChurnRiskFlag`.
  - Use scatter plot or matrix layout to identify high-value high-risk customers.
- Filters and interactivity:
  - Global dashboard filters for `CreditRiskBand` and `ChurnRiskFlag`.
  - Include filters for `Geography` if useful for slicing the risk view.

Data source reference:
- Should connect to `data/processed/bank_analytics_ready.csv`.
- Ensure engineered fields are available: `RFM_Score`, `AgeGroup`, `BalanceSegment`, `CLV_Score`, `ChurnRiskFlag`, `CreditRiskBand`.
