import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import yfinance as yf
from datetime import datetime

# 1. Page Configuration (Must be first)
st.set_page_config(
    page_title="Apex Wealth Executive Dashboard",
    page_icon="💳",
    layout="wide"  # Forces full-screen desktop alignment
)

# 2. Advanced CSS styling for a cohesive layout grid
st.html("""
    <style>
    /* App-wide styling */
    .stApp { background-color: #F8F9FA; }
    
    /* Clean Cards for Metrics */
    .metric-box {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.04);
        border-left: 5px solid #6C757D;
        margin-bottom: 15px;
    }
    .metric-box-title { color: #6C757D; font-size: 13px; font-weight: 600; text-transform: uppercase; }
    .metric-box-value { color: #212529; font-size: 24px; font-weight: 700; margin-top: 5px; }
    
    /* 50/30/20 Border Themes */
    .border-needs { border-left-color: #1A5F7A !important; }
    .border-wants { border-left-color: #D49B35 !important; }
    .border-savings { border-left-color: #226F54 !important; }
    
    /* White Card Blocks for Lists and Forms */
    .dashboard-block {
        background-color: #FFFFFF;
        padding: 22px;
        border-radius: 12px;
        border: 1px solid #E9ECEF;
        margin-bottom: 20px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.02);
    }
    </style>
""")

# Initialize transaction session state if not existing
if "transactions" not in st.session_state:
    st.session_state.transactions = pd.DataFrame([
        {"Date": "2026-06-10", "Category": "Salary", "Amount": 6500.00, "Notes": "Monthly Take-Home Pay"},
        {"Date": "2026-06-12", "Category": "Rent/Utilities", "Amount": -1800.00, "Notes": "Apartment Lease"},
        {"Date": "2026-06-14", "Category": "Groceries", "Amount": -250.00, "Notes": "Weekly Essentials"},
        {"Date": "2026-06-15", "Category": "Dining Out", "Amount": -120.00, "Notes": "Weekend Dinner"}
    ])

# ==============================================================================
# HEADER SECTION
# ==============================================================================
st.title("💳 Executive Wealth Dashboard")
st.markdown("##### Consolidated Financial Strategy & Analytics Portfolio")
st.divider()

# ==============================================================================
# ROW 1: MASTER METRIC TILES (4 Column Grid)
# ==============================================================================
income_sum = st.session_state.transactions[st.session_state.transactions['Amount'] > 0]['Amount'].sum()
expense_sum = abs(st.session_state.transactions[st.session_state.transactions['Amount'] < 0]['Amount'].sum())
liquid_cash = income_sum - expense_sum
investments_total = 45000.00  # Baseline investment mock assets
net_worth = liquid_cash + investments_total

m_col1, m_col2, m_col3, m_col4 = st.columns(4)
with m_col1:
    st.html(f'<div class="metric-box" style="border-left-color:#212529;"><div class="metric-box-title">Total Net Worth</div><div class="metric-box-value">${net_worth:,.2f}</div></div>')
with m_col2:
    st.html(f'<div class="metric-box" style="border-left-color:#2E7D32;"><div class="metric-box-title">Total Inflows</div><div class="metric-box-value">${income_sum:,.2f}</div></div>')
with m_col3:
    st.html(f'<div class="metric-box" style="border-left-color:#C62828;"><div class="metric-box-title">Total Outflows</div><div class="metric-box-value">${expense_sum:,.2f}</div></div>')
with m_col4:
    st.html(f'<div class="metric-box" style="border-left-color:#1A73E8;"><div class="metric-box-title">Invested Base Assets</div><div class="metric-box-value">${investments_total:,.2f}</div></div>')

st.write("---")

# ==============================================================================
# ROW 2: 50/30/20 BUDGETING SECTION (Balanced Side-by-Side Grid)
# ==============================================================================
st.subheader("🎯 The 50/30/20 Capital Allocation Allocation")

budget_col_left, budget_col_right = st.columns([5, 4], gap="large")

with budget_col_left:
    income_input = st.number_input("Adjust Monthly Net Income Base ($)", min_value=100.0, value=6500.0, step=500.0)
    
    needs_val = income_input * 0.50
    wants_val = income_input * 0.30
    savings_val = income_input * 0.20
    
    # Nested Columns for Budget Category Cards
    sub_c1, sub_c2, sub_c3 = st.columns(3)
    with sub_c1:
        st.html(f'<div class="metric-box border-needs"><div class="metric-box-title">Needs (50%)</div><div class="metric-box-value">${needs_val:,.2f}</div></div>')
    with sub_c2:
        st.html(f'<div class="metric-box border-wants"><div class="metric-box-title">Wants (30%)</div><div class="metric-box-value">${wants_val:,.2f}</div></div>')
    with sub_c3:
        st.html(f'<div class="metric-box border-savings"><div class="metric-box-title">Savings (20%)</div><div class="metric-box-value">${savings_val:,.2f}</div></div>')

    # Custom Donut Allocation Graphic
    fig_donut = go.Figure(data=[go.Pie(
        labels=['Essential Needs', 'Discretionary Wants', 'Future Savings'],
        values=[needs_val, wants_val, savings_val],
        hole=.6,
        marker=dict(colors=['#1A5F7A', '#D49B35', '#226F54'], line=dict(color='#FFFFFF', width=2)),
        hoverinfo='label+percent', textinfo='percent'
    )])
    fig_donut.update_layout(margin=dict(t=10, b=10, l=10, r=10), height=260, legend=dict(orientation="h", y=-0.1))
    st.plotly_chart(fig_donut, use_container_width=True)

with budget_col_right:
    st.markdown("##### Real-Life Allocation Guidelines")
    sub_tabs = st.tabs(["🏠 Needs Use-Cases", "🎉 Wants Use-Cases", "💰 Savings Guide"])
    
    with sub_tabs[0]:
        st.html(f'<div class="dashboard-block"><b>Essentials:</b> Use this ${needs_val:,.2f} strictly for rent/mortgage, baseline groceries, utilities, health insurance, and minimum legal loan servicing.</div>')
    with sub_tabs[1]:
        st.html(f'<div class="dashboard-block"><b>Lifestyle Limits:</b> Cap your fine dining, retail purchases, concerts, and luxury subscriptions safely underneath ${wants_val:,.2f} every month.</div>')
    with sub_tabs[2]:
        st.html(f'<div class="dashboard-block"><b>Wealth Engine:</b> Route this ${savings_val:,.2f} directly into a high-yield emergency account or index fund ETFs (e.g., S&P 500) before spending anything else.</div>')

st.write("---")

# ==============================================================================
# ROW 3: TRANSACTIONS & LIVE MARKET ANALYSIS
# ==============================================================================
col_ledger, col_market = st.columns([1, 1], gap="large")

with col_ledger:
    st.subheader("📊 Transaction Management")
    with st.expander("➕ Log New Transaction Entry", expanded=False):
        with st.form("ledger_form", clear_on_submit=True):
            f_date = st.date_input("Date", datetime.now())
            f_cat = st.selectbox("Category", ["Salary", "Groceries", "Dining Out", "Rent/Utilities", "Investments", "Other"])
            f_amt = st.number_input("Amount ($ Value)", value=0.0, step=50.0, help="Use negative numbers for your expenses.")
            f_note = st.text_input("Vendor / Notes")
            
            if st.form_submit_button("Commit to Ledger"):
                new_txn = {"Date": str(f_date), "Category": f_cat, "Amount": f_amt, "Notes": f_note}
                st.session_state.transactions = pd.concat([st.session_state.transactions, pd.DataFrame([new_txn])], ignore_index=True)
                st.rerun()

    st.dataframe(st.session_state.transactions.sort_values(by="Date", ascending=False), use_container_width=True, hide_index=True)

with col_market:
    st.subheader("📈 Live Market Tracker")
    ticker = st.text_input("Enter Ticker Symbol Code:", "AAPL").upper().strip()
    if ticker:
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period="1mo")
            if not hist.empty:
                c_p = hist['Close'].iloc[-1]
                p_p = hist['Close'].iloc[-2]
                chg = c_p - p_p
                chg_pct = (chg / p_p) * 100
                st.metric(label=f"{ticker} Current Spot", value=f"${c_p:,.2f}", delta=f"${chg:,.2f} ({chg_pct:.2f}%)")
                st.line_chart(hist['Close'], color="#1A5F7A")
            else:
                st.caption("No dynamic pricing found for that symbol code.")
        except Exception:
            st.caption("Ating global indexing connection timeouts.")

st.write("---")

# ==============================================================================
# ROW 4: STRATEGIC SEARCH KNOWLEDGE BASE
# ==============================================================================
st.subheader("🙋‍♂️ Personal Finance Search Consultant")
search_input = st.text_input("Ask a question about your personal finances (e.g., 'inflation', 'emergency fund', 'investing')")

KNOWLEDGE_DATA = {
    "emergency fund": "💡 **Emergency Fund Strategy:** Stash 3-6 months of essential survival expenses inside a High-Yield Savings Account. Do not touch this unless it is an absolute emergency.",
    "investing": "💡 **Investment Philosophy:** Consistently buy broad, low-cost index funds tracking the S&P 500. Avoid timing market peaks; focus instead on steady, long-term wealth building.",
    "inflation": "💡 **Inflation Reality:** Cash losing purchase value can be mitigated by holding appreciating assets like equities, commodities, or global index index investments.",
    "credit score": "💡 **Credit Matrix Optimization:** Secure pristine payment timelines and hold revolving utilization thresholds under 30% of global limits to secure premier interest tiers."
}

if search_input:
    found_key = False
    for keyword, analysis in KNOWLEDGE_DATA.items():
        if keyword in search_input.lower():
            st.info(analysis)
            found_key = True
            break
    if not found_key:
        st.warning("🤖 I didn't recognize those specific keywords. Try searching for standard terms like 'emergency fund', 'investing', or 'inflation'.")
