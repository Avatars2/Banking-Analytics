import os

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import mysql.connector
from dotenv import load_dotenv
from datetime import datetime

# =============================================================================
# 1. Page Configuration
# =============================================================================
st.set_page_config(
    page_title="Executive Banking Analytics Platform",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================================================
# 2. Theme tokens + CSS injection
# =============================================================================
BG = "#0a0e1a"
CARD = "#111827"
CARD_BORDER = "#1f2937"
TEXT_PRIMARY = "#f3f4f6"
TEXT_MUTED = "#9ca3af"
BLUE = "#3b82f6"
GREEN = "#10b981"
ORANGE = "#f59e0b"
PURPLE = "#a855f7"
RED = "#ef4444"

st.markdown(f"""
    <style>
    .stApp {{
        background-color: {BG};
    }}
    [data-testid="stSidebar"] {{
        background-color: {CARD};
        border-right: 1px solid {CARD_BORDER};
    }}
    h1, h2, h3, h4 {{
        font-family: 'Inter', sans-serif !important;
        font-weight: 700 !important;
        letter-spacing: -0.3px;
        color: {TEXT_PRIMARY} !important;
    }}
    p, span, label, div {{
        font-family: 'Inter', sans-serif;
    }}

    /* ---- KPI metric cards ---- */
    [data-testid="stMetricValue"] {{
        font-size: 2rem !important;
        font-weight: 700 !important;
        color: {TEXT_PRIMARY} !important;
    }}
    [data-testid="stMetricLabel"] {{
        font-size: 0.78rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.6px !important;
        color: {TEXT_MUTED} !important;
    }}
    [data-testid="stMetricDelta"] {{
        font-size: 0.85rem !important;
    }}

    /* ---- Custom card wrapper ---- */
    .exec-card {{
        background-color: {CARD};
        border: 1px solid {CARD_BORDER};
        border-radius: 14px;
        padding: 22px 24px;
        margin-bottom: 18px;
    }}
    .exec-card-title {{
        font-size: 1.05rem;
        font-weight: 700;
        color: {TEXT_PRIMARY};
        margin-bottom: 4px;
    }}
    .icon-badge {{
        width: 44px;
        height: 44px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.3rem;
        margin-bottom: 10px;
    }}
    .kpi-label {{
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.6px;
        color: {TEXT_MUTED};
        margin-bottom: 2px;
    }}
    .kpi-value {{
        font-size: 1.9rem;
        font-weight: 700;
        color: {TEXT_PRIMARY};
        line-height: 1.15;
    }}
    .kpi-sub {{
        font-size: 0.82rem;
        color: {TEXT_MUTED};
        margin-top: 2px;
    }}

    /* ---- Insight rows ---- */
    .insight-row {{
        display: flex;
        align-items: flex-start;
        gap: 12px;
        padding: 10px 0;
        border-bottom: 1px solid {CARD_BORDER};
    }}
    .insight-row:last-child {{ border-bottom: none; }}
    .insight-title {{
        font-weight: 600;
        color: {TEXT_PRIMARY};
        font-size: 0.92rem;
    }}
    .insight-sub {{
        color: {TEXT_MUTED};
        font-size: 0.82rem;
    }}

    /* ---- Sidebar nav pill ---- */
    .sidebar-pill {{
        background-color: rgba(59,130,246,0.15);
        border: 1px solid rgba(59,130,246,0.35);
        color: {BLUE};
        border-radius: 10px;
        padding: 10px 14px;
        font-weight: 600;
        font-size: 0.9rem;
        margin-bottom: 18px;
    }}

    hr {{ border-color: {CARD_BORDER} !important; }}

    /* Tighten default streamlit block spacing */
    .block-container {{ padding-top: 1.8rem; }}
    </style>
""", unsafe_allow_html=True)


def icon_badge(emoji, color):
    return f"""<div class="icon-badge" style="background-color:{color}22; color:{color};">{emoji}</div>"""


# =============================================================================
# 3. Data Layer
# =============================================================================
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
load_dotenv(os.path.join(BASE_DIR, ".env"))

@st.cache_data
def load_data():
    db_host = os.getenv("DB_HOST", "localhost")
    db_user = os.getenv("DB_USER", "root")
    db_password = os.getenv("DB_PASSWORD", "")
    db_name = os.getenv("DB_NAME", "banking_analytics")

    query = """
    SELECT 
        c.*, 
        a.RFM_Score, 
        a.AgeGroup, 
        a.BalanceSegment, 
        a.CLV_Score, 
        a.ChurnRiskFlag, 
        a.CreditRiskBand
    FROM customer_churn c
    JOIN customer_analytics a ON c.CustomerId = a.CustomerId;
    """

    try:
        conn = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name,
        )
        df = pd.read_sql(query, conn)
        conn.close()
        print(f"[INFO] Loaded dashboard data from MySQL database '{db_name}'.")
        return df, "MySQL"
    except Exception as exc:
        print(f"[WARN] MySQL data load failed, using processed CSV fallback. Error: {exc}")
        csv_path = os.path.join(BASE_DIR, "data", "processed", "bank_analytics_ready.csv")
        df = pd.read_csv(csv_path)
        return df, "CSV"


try:
    df, data_source = load_data()

    # ----- Sidebar -------------------------------------------------------
    with st.sidebar:
        st.markdown(
            f"""
            <div style="display:flex; align-items:center; gap:10px; margin-bottom:22px;">
                <div style="font-size:1.8rem;">🏦</div>
                <div>
                    <div style="font-weight:700; font-size:1rem; color:{TEXT_PRIMARY};">Executive Banking</div>
                    <div style="font-size:0.78rem; color:{TEXT_MUTED};">Analytics Platform</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.markdown('<div class="sidebar-pill">⚙️ Control Center</div>', unsafe_allow_html=True)

        st.markdown(f'<div style="font-size:0.75rem; letter-spacing:0.6px; color:{TEXT_MUTED}; '
                    f'text-transform:uppercase; margin-bottom:8px;">Filters</div>', unsafe_allow_html=True)

        # Filter 1: Geography Selection
        country_list = list(df["Geography"].unique())
        selected_geo = st.multiselect(
            "Geographic Segment:",
            options=country_list,
            default=country_list
        )

        # Filter 2: Bank Membership Activity Status
        activity_status = st.radio(
            "Customer Activity Type:",
            options=["All Customers", "Active Members Only", "Inactive Members Only"],
            index=0
        )

        st.markdown("---")
        st.markdown(f'<div style="font-size:0.75rem; letter-spacing:0.6px; color:{TEXT_MUTED}; '
                    f'text-transform:uppercase; margin-bottom:10px;">Actions</div>', unsafe_allow_html=True)
        
        # Applying Dynamic Filtering Chains early so it can be downloaded directly
        filtered_df = df[df["Geography"].isin(selected_geo)]
        if activity_status == "Active Members Only":
            filtered_df = filtered_df[filtered_df["IsActiveMember"] == 1]
        elif activity_status == "Inactive Members Only":
            filtered_df = filtered_df[filtered_df["IsActiveMember"] == 0]

        # Convert the filtered data segment cleanly into string formats for easy downloading
        csv_data = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="⬇️ Download Filtered CSV",
            data=csv_data,
            file_name="filtered_banking_report.csv",
            mime="text/csv",
            use_container_width=True
        )
        
        # Real Working Core Cache Refresh Interface
        if st.button("🔄 Clear App Cache", use_container_width=True):
            st.cache_data.clear()
            st.rerun()

        st.markdown("---")
        st.markdown(
            f"""
            <div class="exec-card" style="padding:16px 18px;">
                <div style="font-weight:700; color:{TEXT_PRIMARY}; margin-bottom:6px;">ℹ️ About</div>
                <div style="font-size:0.82rem; color:{TEXT_MUTED}; margin-bottom:10px;">
                    Analytics for executive banking customer portfolios.
                </div>
                <div style="font-size:0.78rem; color:{GREEN};">● Data source: {data_source}</div>
                <div style="font-size:0.78rem; color:{TEXT_MUTED};">Last updated: session load</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # ----- Main Header ------------------------------------------------------
    header_col1, header_col2 = st.columns([4, 1])
    with header_col1:
        st.markdown(
            f"""
            <div style="display:flex; align-items:center; gap:14px;">
                <div style="font-size:2.4rem;">🏦</div>
                <div>
                    <div style="font-size:1.9rem; font-weight:800; color:{TEXT_PRIMARY};">
                        Executive Banking Customer Portfolio Platform
                    </div>
                    <div style="color:{TEXT_MUTED}; font-size:0.95rem; margin-top:2px;">
                        System Status: Live Production Connection &nbsp;&nbsp;◆&nbsp;&nbsp;
                        Target Demographics: Global Retail Portfolios
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with header_col2:
        st.markdown(
            f"""
            <div style="text-align:right; color:{TEXT_MUTED}; padding-top:10px;">
                📅 {datetime.now().strftime('%B %d, %Y')}<br>
                <span style="font-size:0.85rem;">{datetime.now().strftime('%I:%M %p')}</span>
            </div>
            """,
            unsafe_allow_html=True
        )
    st.markdown("<div style='margin-bottom:14px;'></div>", unsafe_allow_html=True)

    # ----- Core Operational KPI Summary -----------------
    total_customers = len(filtered_df)

    if total_customers > 0:
        avg_balance = filtered_df["Balance"].mean()
        churn_rate = (filtered_df["Exited"].sum() / total_customers) * 100
        at_risk = len(filtered_df[(filtered_df["Exited"] == 0) & (filtered_df["IsActiveMember"] == 0)])
    else:
        avg_balance = 0.0
        churn_rate = 0.0
        at_risk = 0

    kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)

    with kpi_col1:
        st.markdown(
            f"""<div class="exec-card">
                    {icon_badge("👥", BLUE)}
                    <div class="kpi-label">Active Portfolio Volume</div>
                    <div class="kpi-value">{total_customers:,}</div>
                    <div class="kpi-sub">Total Customers</div>
                </div>""",
            unsafe_allow_html=True
        )
    with kpi_col2:
        st.markdown(
            f"""<div class="exec-card">
                    {icon_badge("💰", GREEN)}
                    <div class="kpi-label">Mean Capital Balance</div>
                    <div class="kpi-value">${avg_balance:,.2f}</div>
                    <div class="kpi-sub">Average Balance</div>
                </div>""",
            unsafe_allow_html=True
        )
    with kpi_col3:
        st.markdown(
            f"""<div class="exec-card">
                    {icon_badge("📉", ORANGE)}
                    <div class="kpi-label">Observed Loss Rate</div>
                    <div class="kpi-value">{churn_rate:.1f}%</div>
                    <div class="kpi-sub">Customer Churn Rate</div>
                </div>""",
            unsafe_allow_html=True
        )
    with kpi_col4:
        st.markdown(
            f"""<div class="exec-card">
                    {icon_badge("⚠️", PURPLE)}
                    <div class="kpi-label">At-Risk Customers</div>
                    <div class="kpi-value">{at_risk:,}</div>
                    <div class="kpi-sub">Retained &amp; Inactive</div>
                </div>""",
            unsafe_allow_html=True
        )

    # ----- High Risk / Credit Risk Visualizations --------------------------
    high_risk_df = filtered_df[filtered_df["ChurnRiskFlag"] == "High Risk"]
    high_risk_count = len(high_risk_df)
    high_risk_avg_clv = high_risk_df["CLV_Score"].mean() if high_risk_count > 0 else 0.0

    risk_chart_col, age_chart_col, summary_col = st.columns([1.4, 1.4, 1])

    with summary_col:
        st.markdown('<div class="exec-card">', unsafe_allow_html=True)
        st.markdown('<div class="exec-card-title">🧠 High Risk Customer Summary</div>', unsafe_allow_html=True)
        st.markdown(
            f"""<div style='display:flex; flex-direction:column; gap:14px;'>
                    <div style='color:{TEXT_MUTED}; font-size:0.88rem;'>High Risk Customer Count</div>
                    <div style='color:{TEXT_PRIMARY}; font-size:2rem; font-weight:700;'>{high_risk_count:,}</div>
                    <div style='color:{TEXT_MUTED}; font-size:0.88rem; margin-top:8px;'>Average High Risk CLV</div>
                    <div style='color:{GREEN}; font-size:2rem; font-weight:700;'>${high_risk_avg_clv:,.2f}</div>
                </div>""",
            unsafe_allow_html=True
        )
        st.markdown('</div>', unsafe_allow_html=True)

    with risk_chart_col:
        st.markdown('<div class="exec-card">', unsafe_allow_html=True)
        st.markdown('<div class="exec-card-title">📊 Churn Rate by Credit Risk Band</div>', unsafe_allow_html=True)

        band_order = ["Poor", "Fair", "Good", "Very Good", "Exceptional"]
        filtered_df["CreditRiskBand"] = pd.Categorical(
            filtered_df["CreditRiskBand"], categories=band_order, ordered=True
        )
        churn_rate_df = (
            filtered_df.groupby("CreditRiskBand", observed=True)["Exited"]
            .mean()
            .mul(100)
            .reset_index()
            .rename(columns={"Exited": "ChurnRatePct"})
        )
        churn_rate_df = churn_rate_df.dropna(subset=["CreditRiskBand"])

        fig_churn = px.bar(
            churn_rate_df,
            x="CreditRiskBand",
            y="ChurnRatePct",
            color="CreditRiskBand",
            color_discrete_sequence=[RED, ORANGE, GREEN, BLUE, PURPLE],
            labels={"ChurnRatePct": "Churn Rate (%)", "CreditRiskBand": "Credit Risk Band"},
        )
        fig_churn.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            showlegend=False,
            xaxis_title=None,
            yaxis_title="Churn Rate (%)",
            margin=dict(t=10, b=20, l=10, r=10),
            font=dict(color=TEXT_MUTED),
        )
        st.plotly_chart(fig_churn, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with age_chart_col:
        st.markdown('<div class="exec-card">', unsafe_allow_html=True)
        st.markdown('<div class="exec-card-title">👥 Age Group Segmentation & Risk</div>', unsafe_allow_html=True)

        age_order = ["18-30", "31-45", "46-60", "60+"]
        age_df = (
            filtered_df.groupby("AgeGroup", observed=True)
            .agg(Customer_Count=("CustomerId", "count"), Churned_Count=("Exited", "sum"))
            .reset_index()
        )
        age_df["AgeGroup"] = pd.Categorical(age_df["AgeGroup"], categories=age_order, ordered=True)
        age_df = age_df.sort_values("AgeGroup")

        fig_age = px.bar(
            age_df,
            x="AgeGroup",
            y=["Customer_Count", "Churned_Count"],
            barmode="group",
            labels={"value": "Count", "AgeGroup": "Age Group", "variable": "Measure"},
            color_discrete_sequence=[BLUE, RED],
        )
        fig_age.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            legend=dict(orientation="h", y=-0.2, font=dict(color=TEXT_MUTED)),
            xaxis_title=None,
            yaxis_title="Customer Count",
            margin=dict(t=10, b=10, l=10, r=10),
            font=dict(color=TEXT_MUTED),
        )
        st.plotly_chart(fig_age, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ----- Advanced Analytics Grid -----------------------------------------
    left_chart_col, right_chart_col = st.columns(2)

    with left_chart_col:
        st.markdown('<div class="exec-card">', unsafe_allow_html=True)
        st.markdown('<div class="exec-card-title">🗺️ Portfolio Breakdown by Region</div>', unsafe_allow_html=True)

        geo_count = filtered_df["Geography"].value_counts().reset_index()
        geo_count.columns = ["Country", "Active Customer Count"]

        fig1 = px.pie(
            geo_count, names="Country", values="Active Customer Count", hole=0.62,
            color_discrete_sequence=[BLUE, "#22d3ee", ORANGE, PURPLE, GREEN]
        )
        fig1.update_traces(
            textinfo="percent",
            textfont_size=13,
            textfont_color="white",
            marker=dict(line=dict(color=CARD, width=3))
        )
        fig1.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            showlegend=True,
            legend=dict(orientation="v", font=dict(color=TEXT_MUTED, size=12)),
            margin=dict(t=10, b=10, l=10, r=10),
            annotations=[dict(
                text=f"{total_customers:,}<br><span style='font-size:12px;color:{TEXT_MUTED}'>Total</span>",
                x=0.5, y=0.5, font=dict(size=20, color=TEXT_PRIMARY, family="Inter"), showarrow=False
            )]
        )
        st.plotly_chart(fig1, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with right_chart_col:
        st.markdown('<div class="exec-card">', unsafe_allow_html=True)
        st.markdown('<div class="exec-card-title">⚠️ Financial Balance Risk Spread</div>', unsafe_allow_html=True)

        plot_df = filtered_df.copy()
        plot_df["Status"] = plot_df["Exited"].map({0: "Retained Portfolio", 1: "Churned Portfolio"})

        fig2 = px.box(
            plot_df, x="Status", y="Balance", color="Status",
            color_discrete_map={"Retained Portfolio": GREEN, "Churned Portfolio": RED}
        )
        fig2.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            yaxis_gridcolor=CARD_BORDER,
            xaxis_title=None,
            showlegend=False,
            font=dict(color=TEXT_MUTED),
            margin=dict(t=10, b=10, l=10, r=10)
        )
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ----- Bottom row: segment table + key insights ------------------------
    table_col, insight_col = st.columns([1.4, 1])

    with table_col:
        st.markdown('<div class="exec-card">', unsafe_allow_html=True)
        st.markdown('<div class="exec-card-title">📋 Top Customer Segments by Balance</div>', unsafe_allow_html=True)

        if total_customers > 0:
            seg_df = filtered_df.copy()
            seg_df["Segment"] = pd.qcut(
                seg_df["Balance"].rank(method="first"),
                q=4,
                labels=["Emerging Affluent", "Mass Affluent", "Affluent", "High Net Worth"]
            )
            seg_summary = seg_df.groupby("Segment", observed=True).agg(
                Customers=("Balance", "count"),
                Total_Balance=("Balance", "sum"),
                Avg_Balance=("Balance", "mean"),
                Churn_Rate=("Exited", "mean")
            ).reset_index()
            seg_summary = seg_summary.sort_values("Total_Balance", ascending=False)
            seg_summary["Total_Balance"] = seg_summary["Total_Balance"].map(lambda v: f"${v:,.0f}")
            seg_summary["Avg_Balance"] = seg_summary["Avg_Balance"].map(lambda v: f"${v:,.0f}")
            seg_summary["Churn_Rate"] = seg_summary["Churn_Rate"].map(lambda v: f"{v*100:.1f}%")
            seg_summary.columns = ["Segment", "Customers", "Total Balance", "Avg Balance", "Churn Rate"]

            st.dataframe(seg_summary, hide_index=True, use_container_width=True)
        else:
            st.info("No customers match the current filters.")
        st.markdown('</div>', unsafe_allow_html=True)

    with insight_col:
        st.markdown('<div class="exec-card">', unsafe_allow_html=True)
        st.markdown('<div class="exec-card-title">💡 Key Insights</div>', unsafe_allow_html=True)

        if total_customers > 0:
            top_geo = geo_count.sort_values("Active Customer Count", ascending=False).iloc[0]["Country"]
            churn_by_geo = filtered_df.groupby("Geography")["Exited"].mean().sort_values(ascending=False)
            worst_geo = churn_by_geo.index[0] if len(churn_by_geo) else "N/A"
            worst_geo_rate = churn_by_geo.iloc[0] * 100 if len(churn_by_geo) else 0
        else:
            top_geo, worst_geo, worst_geo_rate = "N/A", "N/A", 0

        insights = [
            ("📈", GREEN, "Largest Segment", f"{top_geo} holds the largest share of the active portfolio."),
            ("⚠️", ORANGE, "Highest Churn Region", f"{worst_geo} shows the highest observed loss rate at {worst_geo_rate:.1f}%."),
            ("👥", PURPLE, "Retention Focus", f"{at_risk:,} retained customers are currently inactive members."),
        ]
        rows_html = ""
        for emoji, color, title, sub in insights:
            rows_html += f"""
            <div class="insight-row">
                {icon_badge(emoji, color)}
                <div>
                    <div class="insight-title">{title}</div>
                    <div class="insight-sub">{sub}</div>
                </div>
            </div>"""
        st.markdown(rows_html, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

except Exception as e:
    st.error(f"Critical error loading dataset matrix: {e}")