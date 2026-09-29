# Banking Customer Analytics System

Analyze banking transactions and customer activity data to generate business
insights — customer segmentation, transaction analysis, loan analytics, and
customer lifetime value.

## Tech Stack
- Python (pandas, Streamlit, Plotly)
- MySQL
- Tableau

## Folder Structure
```
Banking_Customer_Analytics_System/
├── data/
│   ├── raw/                # Original, untouched source data
│   │   └── Churn_Modelling.csv
│   └── processed/          # Cleaned / transformed data ready for analysis
│       └── bank_analytics_ready.csv
├── scripts/
│   ├── feature_engineering.py # Generates engineered RFM / CLV features
│   ├── upload.py              # Loads raw CSV data into MySQL (legacy)
│   └── upload_processed.py    # Bulk loads processed analytics dataset into MySQL
├── dashboard/
│   └── app.py                 # Streamlit executive analytics dashboard
├── sql/
│   ├── schema.sql             # MySQL schema and analytics tables
│   └── analysis_queries.sql   # Business intelligence analytics queries
├── tableau/
│   ├── Customer_Insights_Dashboard.twb
│   └── Risk_Assessment_Dashboard.twb
├── docs/
│   ├── 1_Project_Metadata.pdf
│   ├── tableau_dashboard_guide.md
│   ├── Insights_Summary.md
│   └── screenshots/           # Store dashboard screenshot assets here
├── .env.example               # Template for DB credentials — copy to .env
├── .gitignore
├── requirements.txt
└── README.md
```

## Methodology & Formula Proxy
This project uses proxy models to approximate customer behavior from the static
banking dataset. Because the provided data is a single snapshot rather than a
full transaction ledger, the engineered features use available fields to
estimate customer value, engagement, and churn risk.

- **Proxy RFM Scoring:** We use `Tenure` as a proxy for Recency, `NumOfProducts`
as a proxy for Frequency, and `Balance + EstimatedSalary` as a proxy for
Monetary value. Each proxy variable is converted into a 1–5 quintile score
using `pandas.qcut`, then summed to create the final `RFM_Score`.
- **RFM Score Range:** Because the final score is the sum of three quintile
components, it ranges from 3 to 15 and provides a simple segmentation metric
for customer value and engagement.
- **Proxy CLV Formula:** The Customer Lifetime Value proxy is computed as:

```math
\text{CLV\_Score} = \frac{\text{Balance} \times \text{Tenure} \times \text{NumOfProducts}}{100}
```

This formula captures long-term customer value by weighting stored balance,
bank longevity, and product engagement. It is intentionally simple and
interpretable for analytics review, while still differentiating higher-value
customers from lower-value ones.

## Dashboard Preview
The project supports adding dashboard screenshots to help reviewers verify the
visual outputs. Place screenshot images inside `docs/screenshots/` and reference
them directly in this README.

Example screenshot assets:
- `docs/screenshots/customer_insights.png`
- `docs/screenshots/risk_assessment.png`

Embedded preview examples:

![Customer Insights Dashboard](docs/screenshots/customer_insights.png)

![Risk Assessment Dashboard](docs/screenshots/risk_assessment.png)

## Setup

1. Create a virtual environment and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up your database credentials:
   ```bash
   cp .env.example .env
   # then edit .env with your real MySQL password
   ```

3. Load processed analytics data into MySQL:
   ```bash
   python scripts/upload_processed.py
   ```

4. Run the dashboard:
   ```bash
   cd dashboard
   streamlit run app.py
   ```
   *(Note: The dashboard will seamlessly fall back to using `data/processed/bank_analytics_ready.csv` if a database connection is not provided or unavailable.)*

5. Open the `.twb` files in `tableau/` with Tableau Desktop for the
   dashboard views:
   - `Customer_Insights_Dashboard.twb`
   - `Risk_Assessment_Dashboard.twb`

## Security Note
The original `upload.py` had a MySQL password hardcoded in the file. This
has been fixed — credentials are now read from a local `.env` file (which
is git-ignored) instead of being committed to source control.
