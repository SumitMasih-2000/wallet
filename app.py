import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import yfinance as yf
from datetime import datetime

# 1. Page Configuration (Must be first)
st.set_page_config(
    page_title="Aegis Wealth Management Platform",
    page_icon="👑",
    layout="wide"  # Forces full-screen desktop alignment
)

# 2. Advanced CSS styling for an Elite Corporate Canvas Layout
st.html("""
    <style>
    /* Main Background & Font Canvas */
    .stApp { 
        background-color: #F1F3F5 !important; 
    }
    
    /* Clean Cards for Metrics */
    .metric-box {
        background-color: #FFFFFF;
        padding: 22px;
        border-radius: 12px;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.05);
        border-left: 6px solid #4A5568;
        margin-bottom: 15px;
    }
    .metric-box-title { 
        color: #718096; 
        font-size: 13px; 
        font-weight: 600; 
        text-transform: uppercase; 
        letter-spacing: 0.5px;
    }
    .metric-box-value { 
        color: #1A202C; 
        font-size: 26px; 
        font-weight: 700; 
        margin-top: 6px; 
    }
    
    /* 50/30/20 Border Corporate Themes */
    .border-needs { border-left-color: #1A5F7A !important; }
    .border-wants { border-left-color: #D49B35 !important; }
    .border-savings { border-left-color: #226F54 !important; }
    
    /* White Card Blocks for Lists and Forms */
    .dashboard-block {
        background-color: #FFFFFF;
        padding: 24px;
        border-radius: 12px;
        border: 1px solid #E2E8F0;
        margin-bottom: 20px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.03);
    }
    </style>
""")

# Initialize transaction session state if not existing
if "transactions" not in st.session_state:
    st.session_state.transactions = pd.DataFrame([
        {"Date": "2026-06-10", "Category": "Salary", "Amount": 150000.00, "Notes": "Monthly Executive Salary"},
        {"Date": "2026-06-12", "Category": "Rent/Utilities", "Amount": -45000.00, "Notes": "Corporate Suite Lease"},
        {"Date": "2026-06-14", "Category": "Groceries", "Amount": -12000.00, "Notes": "Premium Essentials"},
        {"Date": "2026-06-15", "Category": "Dining Out", "Amount": -6500.00, "Notes": "Client Business Dinner"}
    ])

# ==============================================================================
# HEADER & GLOBAL CONFIGURATION SECTION
# ==============================================================================
st.title("👑 Aegis Wealth Management Platform")
st.markdown("##### Sovereign Portfolio Operations & Institutional Capital Allocation")

# Currency Map Setup
currency_options = {
    "INR (₹)": "₹",
    "USD ($)": "$",
    "EUR (€)": "€",
    "GBP (£)": "£",
    "JPY (¥)": "¥"
}

# Currency selector placed neatly at the header level
cc_col1, cc_col2 = st.columns([3, 1])
with cc_col2:
    selected_currency_label = st.selectbox(
        "Preferred Platform Currency", 
        options=list(currency_options.keys()), 
        index=0 # INR is index 0, making it the strict default
    )
    symbol = currency_options[selected_currency_label]

st.divider()

# ==============================================================================
# ROW 1: MASTER METRIC TILES (4 Column Grid)
# ==============================================================================
income_sum = st.session_state.transactions[st.session_state.transactions['Amount'] > 0]['Amount'].sum()
expense_sum = abs(st.session_state.transactions[st.session_state.transactions['Amount'] < 0]['Amount'].sum())
liquid_cash = income_sum - expense_sum
investments_total = 2500000.00  # Baseline investment mock assets base changed to align with typical INR scales
net_worth = liquid_cash + investments_total

m_col1, m_col2, m_col3, m_col4 = st.columns(4)
with m_col1:
    st.html(f'<div class="metric-box" style="border-left-color:#1A202C;"><div class="metric-box-title">Total Liquidity Net Worth</div><div class="metric-box-value">{symbol}{net_worth:,.2f}</div></div>')
with m_col2:
    st.html(f'<div class="metric-box" style="border-left-color:#226F54;"><div class="metric-box-title">Aggregated Inflows</div><div class="metric-box-value">{symbol}{income_sum:,.2f}</div></div>')
with m_col3:
    st.html(f'<div class="metric-box" style="border-left-color:#A020F0;"><div class="metric-box-title">Aggregated Outflows</div><div class="metric-box-value">{symbol}{expense_sum:,.2f}</div></div>')
with m_col4:
    st.html(f'<div class="metric-box" style="border-left-color:#1A5F7A;"><div class="metric-box-title">Sovereign Asset Base</div><div class="metric-box-value">{symbol}{investments_total:,.2f}</div></div>')

st.write("---")

# ==============================================================================
# ROW 2: 50/30/20 BUDGETING SECTION (Balanced Side-by-Side Grid)
# ==============================================================================
st.subheader("🎯 Tactical 50/30/20 Budget Matrix")

budget_col_left, budget_col_right = st.columns([5, 4], gap="large")

with budget_col_left:
    income_input = st.number_input(f"Adjust Capital Net Income Base ({symbol})", min_value=100.0, value=150000.0, step=5000.0)
    
    needs_val = income_input * 0.50
    wants_val = income_input * 0.30
    savings_val = income_input * 0.20
    
    # Nested Columns for Budget Category Cards
    sub_c1, sub_c2, sub_c3 = st.columns(3)
    with sub_c1:
        st.html(f'<div class="metric-box border-needs"><div class="metric-box-title">Essential Needs (50%)</div><div class="metric-box-value">{symbol}{needs_val:,.2f}</div></div>')
    with sub_c2:
        st.html(f'<div class="metric-box border-wants"><div class="metric-box-title">Flexible Wants (30%)</div><div class="metric-box-value">{symbol}{wants_val:,.2f}</div></div>')
    with sub_c3:
        st.html(f'<div class="metric-box border-savings"><div class="metric-box-title">Strategic Savings (20%)</div><div class="metric-box-value">{symbol}{savings_val:,.2f}</div></div>')

    # Custom Donut Allocation Graphic
    fig_donut = go.Figure(data=[go.Pie(
        labels=['Essential Needs', 'Discretionary Wants', 'Future Savings'],
        values=[needs_val, wants_val, savings_val],
        hole=.6,
        marker=dict(colors=['#1A5F7A', '#D49B35', '#226F54'], line=dict(color='#FFFFFF', width=2)),
        hoverinfo='label+percent', textinfo='percent'
    )])
    fig_donut.update_layout(margin=dict(t=10, b=10, l=10, r=10), height=260, legend=dict(orientation="h", y=-0.1), paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_donut, use_container_width=True)

with budget_col_right:
    st.markdown("##### Asset Allocation Blueprint")
    sub_tabs = st.tabs(["🏠 Needs Use-Cases", "🎉 Wants Use-Cases", "💰 Savings Guide"])
    
    with sub_tabs[0]:
        st.html(f'<div class="dashboard-block"><b>Primary Fixed Obligations:</b> Allocate this {symbol}{needs_val:,.2f} explicitly for real estate/mortgage coverage, core culinary provisions, utility networks, health premiums, and baseline credit maintenance.</div>')
    with sub_tabs[1]:
        st.html(f'<div class="dashboard-block"><b>Lifestyle Allowances:</b> Cap discretionary expenditure profiles including high-end gastronomy, personal commerce, event entry tokens, and luxury recurring entertainment subscriptions under {symbol}{wants_val:,.2f} per term.</div>')
    with sub_tabs[2]:
        st.html(f'<div class="dashboard-block"><b>Capital Accumulation:</b> Direct this {symbol}{savings_val:,.2f} seamlessly into high-yield liquidity reserves or tax-advantaged index trackers (e.g., S&P 500 ETF structures) to harness compounding growth vectors.</div>')

st.write("---")

# ==============================================================================
# ROW 3: TRANSACTIONS & LIVE MARKET ANALYSIS
# ==============================================================================
col_ledger, col_market = st.columns([1, 1], gap="large")

with col_ledger:
    st.subheader("📊 Transaction Ledger Management")
    with st.expander("➕ Log New Transaction Matrix", expanded=False):
        with st.form("ledger_form", clear_on_submit=True):
            f_date = st.date_input("Date", datetime.now())
            f_cat = st.selectbox("Category", ["Salary", "Groceries", "Dining Out", "Rent/Utilities", "Investments", "Other"])
            f_amt = st.number_input(f"Amount ({symbol} Value)", value=0.0, step=500.0, help="Represent outbound balance reductions using negative signs.")
            f_note = st.text_input("Counterparty Vendor / Reference Notes")
            
            if st.form_submit_button("Commit to Ledger"):
                new_txn = {"Date": str(f_date), "Category": f_cat, "Amount": f_amt, "Notes": f_note}
                st.session_state.transactions = pd.concat([st.session_state.transactions, pd.DataFrame([new_txn])], ignore_index=True)
                st.rerun()

    # Formatted version of the dataframe to explicitly include currency symbols
    display_df = st.session_state.transactions.copy()
    display_df['Amount'] = display_df['Amount'].map(lambda x: f"{symbol}{x:,.2f}" if x >= 0 else f"-{symbol}{abs(x):,.2f}")
    
    st.dataframe(display_df.sort_values(by="Date", ascending=False), use_container_width=True, hide_index=True)

with col_market:
    st.subheader("📈 Institutional Equity Tracker")
    ticker = st.text_input("Enter Equity Ticker Code Symbol:", "AAPL").upper().strip()
    if ticker:
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period="1mo")
            if not hist.empty:
                c_p = hist['Close'].iloc[-1]
                p_p = hist['Close'].iloc[-2]
                chg = c_p - p_p
                chg_pct = (chg / p_p) * 100
                
                # Note: Exchange market data generally renders natively in ticker exchange currency currency ($ for AAPA etc.)
                st.metric(label=f"{ticker} Current Spot Value (Exchange Source Denominated)", value=f"${c_p:,.2f}", delta=f"${chg:,.2f} ({chg_pct:.2f}%)")
                st.line_chart(hist['Close'], color="#1A5F7A")
            else:
                st.caption("No dynamic pricing found for that symbol code.")
        except Exception:
            st.caption("Ating global indexing connection timeouts.")

st.write("---")

# ==============================================================================
# ROW 4: STRATEGIC SEARCH KNOWLEDGE BASE
# ==============================================================================
st.subheader("🙋‍♂️ Elite Asset Advisory Consultant")
search_input = st.text_input("Query our structural analytics engine for tailored wealth protocols:")

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
        st.warning("🤖 System Advice: No direct semantic map detected. Try queries utilizing clear keywords such as 'emergency fund', 'investing', or 'inflation'.")
