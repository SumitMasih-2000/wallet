import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import yfinance as yf
from datetime import datetime

# ==============================================================================
# 1. GLOBAL APP CONFIGURATION & MASTER THEME (CSS)
# ==============================================================================
st.set_page_config(
    page_title="Apex Wealth Wallet",
    page_icon="💳",
    layout="wide"
)

# Custom Enterprise-level CSS Inject
st.html("""
    <style>
    /* App Canvas Background */
    .stApp { background-color: #F8F9FA; }
    
    /* Executive Metric Card Styles */
    .metric-card {
        background-color: #FFFFFF;
        padding: 22px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
        border-left: 5px solid #6C757D;
        margin-bottom: 15px;
    }
    .card-title {
        color: #6C757D;
        font-size: 13px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 6px;
    }
    .card-value {
        color: #212529;
        font-size: 26px;
        font-weight: 700;
    }
    
    /* 50/30/20 Color Assignments */
    .needs-card { border-left-color: #1A5F7A; }
    .wants-card { border-left-color: #D49B35; }
    .savings-card { border-left-color: #226F54; }
    
    /* Structural Containers */
    .info-container {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #E9ECEF;
    }
    
    /* Make tab font more premium */
    button[data-baseweb="tab"] { font-size: 16px !important; font-weight: 600 !important; }
    </style>
""")

# ==============================================================================
# 2. STATE MANAGEMENT & DATA INITIALIZATION
# ==============================================================================
if "transactions" not in st.session_state:
    st.session_state.transactions = pd.DataFrame([
        {"Date": "2026-06-10", "Category": "Salary", "Amount": 5200.00, "Notes": "Monthly Corporate Paycheck"},
        {"Date": "2026-06-12", "Category": "Rent/Utilities", "Amount": -1500.00, "Notes": "Downtown Apartment"},
        {"Date": "2026-06-14", "Category": "Groceries", "Amount": -185.40, "Notes": "Whole Foods Market"},
        {"Date": "2026-06-15", "Category": "Dining Out", "Amount": -92.00, "Notes": "Steakhouse Client Dinner"}
    ])

# ==============================================================================
# 3. GLOBAL HEADER
# ==============================================================================
st.title("💳 Apex Wealth Management Platform")
st.markdown("##### Real-Time Insights, Strategic Allocations, & Market Analytics")
st.divider()

# Top Navigation Tabs Architecture
tab_home, tab_503020, tab_ledger, tab_market, tab_qa = st.tabs([
    "🏠 Dashboard Home", 
    "📐 50/30/20 Framework", 
    "📊 Transactions Ledger", 
    "📈 Market Analytics", 
    "🙋‍♂️ Financial Advisor Q&A"
])

# ==============================================================================
# TAB 1: DASHBOARD HOME OVERVIEW
# ==============================================================================
with tab_home:
    st.subheader("Financial Assets At A Glance")
    
    # Live aggregated metrics calculations
    cash_in = st.session_state.transactions[st.session_state.transactions['Amount'] > 0]['Amount'].sum()
    cash_out = abs(st.session_state.transactions[st.session_state.transactions['Amount'] < 0]['Amount'].sum())
    
    # Standard Portfolio Mock Balances
    balances = {"Liquid Checking": 3400.00, "High-Yield Savings": 15000.00, "Investment Portfolio": 42000.00}
    net_worth = sum(balances.values())
    
    # Layout Grid
    h_col1, h_col2, h_col3 = st.columns(3)
    with h_col1:
        st.html(f'<div class="metric-card" style="border-left-color:#4A4A4A;"><div class="card-title">Net Capital Value</div><div class="card-value">${net_worth:,.2f}</div></div>')
    with h_col2:
        st.html(f'<div class="metric-card" style="border-left-color:#2E7D32;"><div class="card-title">Total Inflow History</div><div class="card-value">${cash_in:,.2f}</div></div>')
    with h_col3:
        st.html(f'<div class="metric-card" style="border-left-color:#C62828;"><div class="card-title">Total Outflow Expenses</div><div class="card-value">${cash_out:,.2f}</div></div>')
        
    st.write("---")
    
    # Layout Split: Charts & Allocations
    g_col1, g_col2 = st.columns([5, 4], gap="large")
    with g_col1:
        st.write("### Resource Allocation Strategy")
        df_assets = pd.DataFrame(list(balances.items()), columns=["Account Type", "Value"])
        fig_home = px.pie(df_assets, values="Value", names="Account Type", hole=0.5,
                          color_discrete_sequence=['#1A5F7A', '#57C5B6', '#159895'])
        fig_home.update_layout(margin=dict(t=10, b=10, l=10, r=10), height=320)
        st.plotly_chart(fig_home, use_container_width=True)
    with g_col2:
        st.write("### System Status")
        st.info("💡 **Operational Advisory:** Your liquid savings ratio is in optimal boundaries. To maximize yields against purchasing inflation, consider transferring surplus checking limits into index instruments.")

# ==============================================================================
# TAB 2: 50/30/20 BUDGET CALCULATION
# ==============================================================================
with tab_503020:
    st.subheader("Strategic Capital Allocation Calculator")
    
    col_inc_input, _ = st.columns([2, 2])
    with col_inc_input:
        income = st.number_input("Monthly After-Tax Take-Home Pay ($)", min_value=0.0, value=6000.0, step=500.0)

    if income > 0:
        val_needs = income * 0.50
        val_wants = income * 0.30
        val_savings = income * 0.20

        # Dynamic Left Accent Custom Grid 
        b_c1, b_c2, b_c3 = st.columns(3)
        with b_c1:
            st.html(f'<div class="metric-card needs-card"><div class="card-title">Essentials & Needs (50%)</div><div class="card-value">${val_needs:,.2f}</div></div>')
        with b_c2:
            st.html(f'<div class="metric-card wants-card"><div class="card-title">Discretionary Wants (30%)</div><div class="card-value">${val_wants:,.2f}</div></div>')
        with b_c3:
            st.html(f'<div class="metric-card savings-card"><div class="card-title">Financial Goals (20%)</div><div class="card-value">${val_savings:,.2f}</div></div>')

        st.write("---")
        
        # Split Layout: Pie Visual vs Text Tabs
        b_col_graph, b_col_insights = st.columns([5, 4], gap="large")
        with b_col_graph:
            fig_donut = go.Figure(data=[go.Pie(
                labels=['Essential Needs', 'Discretionary Wants', 'Savings / Wealth Accumulation'],
                values=[val_needs, val_wants, val_savings],
                hole=.55,
                marker=dict(colors=['#1A5F7A', '#D49B35', '#226F54'], line=dict(color='#FFFFFF', width=2)),
                hoverinfo='label+percent', textinfo='percent'
            )])
            fig_donut.update_layout(margin=dict(t=10, b=10, l=10, r=10), height=340, legend=dict(orientation="h", y=-0.1))
            st.plotly_chart(fig_donut, use_container_width=True)
            
        with b_col_insights:
            st.write("#### Tactical Implementation Scope")
            sub_tab_n, sub_tab_w, sub_tab_s = st.tabs(["🏠 Needs Scope", "🎉 Wants Scope", "📈 Savings Plan"])
            
            with sub_tab_n:
                st.html(f'<div class="info-container"><b>Essential Liabilities Target Ceiling:</b><br><ul><li>Rent/Housing Base: Max ${income*0.30:,.2f}</li><li>Groceries Supply: ~${val_needs*0.25:,.2f}</li><li>Utilities &amp; Insurance Networks</li></ul></div>')
            with sub_tab_w:
                st.html(f'<div class="info-container"><b>Guilt-Free Personal Lifestyle Spending Cap:</b><br><ul><li>Gastronomy/Dining Out: ~${val_wants*0.40:,.2f}</li><li>SaaS Subscriptions/Entertainment: ~${val_wants*0.10:,.2f}</li><li>Leisure Travel &amp; Apparel Purchases</li></ul></div>')
            with sub_tab_s:
                st.html(f'<div class="info-container"><b>Future Capital Building Targets:</b><br><ul><li>Emergency Buffer: Build out 3 to 6 months expenses safely.</li><li>Broad Index ETFs Minimum Flow: ~${val_savings*0.60:,.2f}</li></ul></div>')

# ==============================================================================
# TAB 3: TRANSACTIONS LEDGER (DATA INGESTION)
# ==============================================================================
with tab_ledger:
    st.subheader("Unified Asset Activity Log")
    
    # Input Processing Form Panel
    with st.form("transaction_entry_form", clear_on_submit=True):
        st.markdown("**Log New Asset/Expense Modification**")
        lf_col1, lf_col2, lf_col3 = st.columns(3)
        inp_date = lf_col1.date_input("Transaction Posting Date", datetime.now())
        inp_cat = lf_col2.selectbox("Financial Cluster Category", ["Salary", "Groceries", "Dining Out", "Rent/Utilities", "Investments", "Other"])
        inp_amt = lf_col3.number_input("Transaction Volume ($ Value)", value=0.0, step=10.0, help="Represent outbound expenditures using negative indicators.")
        inp_note = st.text_input("Operational Ledger Notes / Vendor Specifics")
        
        if st.form_submit_button("Commit Entry To System Ledger"):
            entry_row = {"Date": str(inp_date), "Category": inp_cat, "Amount": inp_amt, "Notes": inp_note}
            st.session_state.transactions = pd.concat([st.session_state.transactions, pd.DataFrame([entry_row])], ignore_index=True)
            st.toast("Data committed successfully!", icon="✅")

    st.write("---")
    st.write("#### Master Transactions History Table")
    st.dataframe(st.session_state.transactions.sort_values(by="Date", ascending=False), use_container_width=True, hide_index=True)

# ==============================================================================
# TAB 4: MARKET INVESTMENTS ANALYSIS
# ==============================================================================
with tab_market:
    st.subheader("Global Security Performance Tracker")
    st.markdown("Real-time pricing indexing pipelines fed via Yahoo Finance Core infrastructure.")
    
    m_col_input, _ = st.columns([2, 2])
    with m_col_input:
        ticker = st.text_input("Security Ticker Identifier Code:", "AAPL").upper().strip()
        
    if ticker:
        try:
            sec_data = yf.Ticker(ticker)
            sec_hist = sec_data.history(period="1mo")
            
            if not sec_hist.empty:
                curr_price = sec_hist['Close'].iloc[-1]
                prev_price = sec_hist['Close'].iloc[-2]
                delta_price = curr_price - prev_price
                delta_pct = (delta_price / prev_price) * 100
                
                st.metric(label=f"Asset Context: {ticker} Closing Spot Value", value=f"${curr_price:,.2f}", delta=f"${delta_price:,.2f} ({delta_pct:.2f}%)")
                
                st.write(f"### {ticker} Historical Valuation Chart (Past 30 Trading Days)")
                st.line_chart(sec_hist['Close'], color="#1A5F7A")
            else:
                st.warning("Invalid security code identifier. Check indexing conventions (e.g., TSLA, MSFT).")
        except Exception as err:
            st.error(f"Upstream Data Connection Error: {err}")

# ==============================================================================
# TAB 5: FINANCIAL ADVISOR Q&A ENGINE
# ==============================================================================
with tab_qa:
    st.subheader("Interactive Financial Strategy Search Engine")
    st.markdown("Query the corporate knowledge index graph for standard capital optimization strategies.")
    
    user_search = st.text_input("Enter Question Keywords Here (e.g., 'inflation', 'emergency fund', 'investing')", placeholder="What is an emergency fund?")
    
    KNOWLEDGE_INDEX = {
        "emergency fund": "**Emergency Contingency Protocols:** Set aside 3-6 months of necessary living parameters inside liquid high-yield cash vehicles (HYSA) before prioritizing aggressive multi-asset deployment.",
        "investing": "**Capital Risk Management Principles:** Focus consistently on automated dollar-cost averaging configurations into broad equities trackers (like S&P 500 equivalents) to insulate portfolio compound velocities over multi-decade cycles.",
        "inflation": "**Purchasing Depreciation Realities:** When economic inflation benchmarks exceed baseline yields, uninvested dormant ledger values effectively leak structural purchasing scale. Equities and hard property hedges mitigate this systemic friction.",
        "credit score": "**Leverage Credit Matrix Optimization:** Secure prompt utility accounts balance clears before statement generation. Keep rolling systemic utilization metrics bounded tightly underneath 30% thresholds."
    }
    
    if user_search:
        search_normalized = user_search.lower()
        match_resolved = False
        
        for index_key, content in KNOWLEDGE_INDEX.items():
            if index_key in search_normalized:
                st.html(f"""
                    <div style="background-color: #E8F0FE; border-left: 5px solid #1A73E8; padding: 18px; border-radius: 8px;">
                        <p style="color:#1A73E8; font-weight:700; margin-bottom: 5px; text-transform: uppercase; font-size:12px;">Matched Domain Index: {index_key}</p>
                        <span style="color:#202124; font-size: 15px;">{content}</span>
                    </div>
                """)
                match_resolved = True
                break
                
        if not match_resolved:
            st.html("""
                <div style="background-color: #FFF0F0; border-left: 5px solid #D93025; padding: 18px; border-radius: 8px;">
                    <p style="color:#D93025; font-weight:700; margin-bottom: 5px; font-size:12px;">No Definitive Index Linkage Matched</p>
                    <span style="color:#202124; font-size: 15px;"><b>Standard System Advice:</b> Try entering foundational strategic concepts like <i>'emergency fund'</i>, <i>'investing'</i>, <i>'inflation'</i>, or <i>'credit score'</i> for structural knowledge readouts.</span>
                </div>
            """)
