import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# 1. Page Configuration
st.set_page_config(
    page_title="Aegis Wealth Management Platform",
    page_icon="👑",
    layout="wide"
)

# 2. Enhanced CSS Layout Grid Engine
st.html("""
    <style>
    /* Main Background Canvas */
    .stApp { background-color: #F1F3F5 !important; }
    
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
    
    /* Structural Border Highlights */
    .border-income { border-left-color: #226F54 !important; }
    .border-expenses { border-left-color: #A020F0 !important; }
    .border-savings { border-left-color: #1A5F7A !important; }
    .border-net { border-left-color: #1A202C !important; }
    
    .border-needs { border-left-color: #1A5F7A !important; }
    .border-wants { border-left-color: #D49B35 !important; }
    
    /* White Content Cards */
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
        {"Date": "2026-06-13", "Category": "Groceries", "Amount": -12000.00, "Notes": "Premium Essentials"},
        {"Date": "2026-06-14", "Category": "Dining Out", "Amount": -8500.00, "Notes": "Business Lunch"},
        {"Date": "2026-06-15", "Category": "Entertainment", "Amount": -5000.00, "Notes": "Streaming & Events"}
    ])

# ==============================================================================
# HEADER & CURRENCY SELECTION
# ==============================================================================
st.title("👑 Aegis Wealth Management Platform")
st.markdown("##### Sovereign Portfolio Operations & Institutional Capital Allocation")

currency_options = {"INR (₹)": "₹", "USD ($)": "$", "EUR (€)": "€", "GBP (£)": "£"}

cc_col1, cc_col2 = st.columns([3, 1])
with cc_col2:
    selected_currency_label = st.selectbox("Preferred Platform Currency", options=list(currency_options.keys()), index=0)
    symbol = currency_options[selected_currency_label]

st.divider()

# ==============================================================================
# MATH COMPUTATIONS FOR REAL-TIME METRICS
# ==============================================================================
total_income = st.session_state.transactions[st.session_state.transactions['Amount'] > 0]['Amount'].sum()
total_expenses = abs(st.session_state.transactions[st.session_state.transactions['Amount'] < 0]['Amount'].sum())

# Net savings calculated directly from real-time cash flow
net_savings_liquid = total_income - total_expenses
mock_invested_base = 2500000.00
calculated_net_worth = net_savings_liquid + mock_invested_base

# ==============================================================================
# ROW 1: MASTER OPERATIONS DASHBOARD TILES
# ==============================================================================
m_col1, m_col2, m_col3, m_col4 = st.columns(4)
with m_col1:
    st.html(f'<div class="metric-box border-income"><div class="metric-box-title">Total Inbound Income</div><div class="metric-box-value">{symbol}{total_income:,.2f}</div></div>')
with m_col2:
    st.html(f'<div class="metric-box border-expenses"><div class="metric-box-title">Total Outbound Expenses</div><div class="metric-box-value">{symbol}{total_expenses:,.2f}</div></div>')
with m_col3:
    st.html(f'<div class="metric-box border-savings"><div class="metric-box-title">Net Unallocated Savings</div><div class="metric-box-value">{symbol}{net_savings_liquid:,.2f}</div></div>')
with m_col4:
    st.html(f'<div class="metric-box border-net"><div class="metric-box-title">Aggregated Net Worth</div><div class="metric-box-value">{symbol}{calculated_net_worth:,.2f}</div></div>')

st.write("---")

# ==============================================================================
# ROW 2: DETAILED EXPENSE SPLITS & 50/30/20 ANALYSIS
# ==============================================================================
col_chart_left, col_budget_right = st.columns([5, 4], gap="large")

with col_chart_left:
    st.subheader("📊 Expense Category Distribution")
    
    df_expenses = st.session_state.transactions[st.session_state.transactions['Amount'] < 0].copy()
    df_expenses['Amount'] = abs(df_expenses['Amount'])
    
    if not df_expenses.empty:
        df_grouped_expenses = df_expenses.groupby('Category', as_index=False)['Amount'].sum()
        
        fig_expense_pie = px.pie(
            df_grouped_expenses, 
            values="Amount", 
            names="Category", 
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.G10
        )
        fig_expense_pie.update_layout(margin=dict(t=10, b=10, l=10, r=10), height=280, legend=dict(orientation="h", y=-0.15))
        st.plotly_chart(fig_expense_pie, use_container_width=True)
    else:
        st.info("No outflow transaction histories present to populate category distribution indexes.")

with col_budget_right:
    st.subheader("🎯 Automated 50/30/20 Plan Matrix")
    income_input = st.number_input(f"Define Reference Salary Base ({symbol})", min_value=100.0, value=150000.0, step=5000.0)
    
    needs_val = income_input * 0.50
    wants_val = income_input * 0.30
    savings_val = income_input * 0.20
    
    sub_c1, sub_c2, sub_c3 = st.columns(3)
    with sub_c1:
        st.html(f'<div class="metric-box border-needs" style="padding:12px;"><div class="metric-box-title" style="font-size:11px;">Needs (50%)</div><div class="metric-box-value" style="font-size:18px;">{symbol}{needs_val:,.0f}</div></div>')
    with sub_c2:
        st.html(f'<div class="metric-box border-wants" style="padding:12px;"><div class="metric-box-title" style="font-size:11px;">Wants (30%)</div><div class="metric-box-value" style="font-size:18px;">{symbol}{wants_val:,.0f}</div></div>')
    with sub_c3:
        st.html(f'<div class="metric-box border-savings" style="padding:12px;"><div class="metric-box-title" style="font-size:11px;">Savings (20%)</div><div class="metric-box-value" style="font-size:18px;">{symbol}{savings_val:,.0f}</div></div>')

st.write("---")

# ==============================================================================
# ROW 3: TRANSACTION MODIFICATION LEDGER
# ==============================================================================
st.subheader("📝 Transaction Modification Ledger")

with st.expander("➕ Log New Transaction Matrix Element", expanded=False):
    with st.form("ledger_form", clear_on_submit=True):
        f_date = st.date_input("Posting Date", datetime.now())
        f_cat = st.selectbox("Financial Node Category", ["Salary", "Groceries", "Dining Out", "Rent/Utilities", "Entertainment", "Investments", "Other"])
        f_amt = st.number_input(f"Value Magnitude ({symbol})", value=0.0, step=500.0, help="Represent expenditures using a negative sign prefix.")
        f_note = st.text_input("Operational Notes / Counterparty Specs")
        
        if st.form_submit_button("Commit Entry to Database"):
            new_txn = {"Date": str(f_date), "Category": f_cat, "Amount": f_amt, "Notes": f_note}
            st.session_state.transactions = pd.concat([st.session_state.transactions, pd.DataFrame([new_txn])], ignore_index=True)
            st.rerun()

# Prepping clean presentation dataframe copy
display_df = st.session_state.transactions.copy()
display_df['Amount'] = display_df['Amount'].map(lambda x: f"{symbol}{x:,.2f}" if x >= 0 else f"-{symbol}{abs(x):,.2f}")
st.dataframe(display_df.sort_values(by="Date", ascending=False), use_container_width=True, hide_index=True)

st.write("---")

# ==============================================================================
# ROW 4: DATA-DRIVEN FINANCIAL ADVISOR CHAT
# ==============================================================================
st.subheader("🙋‍♂️ Aegis Data-Aware Advisory Engine")
st.markdown("Your financial virtual assistant scans your local database metrics to deliver real-time insight answers.")

search_input = st.text_input(
    "Ask a question about your specific data or general finance (e.g., 'What is my highest expense?', 'How much did I spend on groceries?', 'What is inflation?')",
    placeholder="Type your question here..."
)

# Extract structured contextual details from data vectors
df_all = st.session_state.transactions
df_debts = df_all[df_all['Amount'] < 0]

if search_input:
    query = search_input.lower().strip()
    answered = False
    
    # --------------------------------------------------------------------------
    # CRITERIA 1: INTENT IDENTIFICATION - EXPENSE ANALYTICS FROM LIVE LEDGER DATA
    # --------------------------------------------------------------------------
    if "highest" in query or "biggest" in query or "largest" in query or "maximum" in query:
        if not df_debts.empty:
            max_row = df_debts.loc[abs(df_debts['Amount']).idxmax()]
            st.info(f"📊 **Data Analysis Readout:** Your largest individual recorded expense was for **{max_row['Category']}** amounting to **{symbol}{abs(max_row['Amount']):,.2f}** ({max_row['Notes']}) on {max_row['Date']}.")
        else:
            st.info("📊 **Data Analysis Readout:** No outlays or expense vectors detected in the system log database yet.")
        answered = True

    elif "spend" in query or "expense" in query or "cost" in query or "total" in query:
        # Check if user mentioned a specific category in their question
        matched_category = None
        for cat in df_all['Category'].unique():
            if cat.lower() in query:
                matched_category = cat
                break
                
        if matched_category:
            cat_sum = abs(df_all[df_all['Category'] == matched_category]['Amount'].sum())
            st.info(f"📊 **Data Analysis Readout:** Your cumulative recorded allocation for **{matched_category}** currently aggregates to **{symbol}{cat_sum:,.2f}**.")
        else:
            st.info(f"📊 **Data Analysis Readout:** Your global outbound operating expense total across all data points combined is **{symbol}{total_expenses:,.2f}**.")
        answered = True

    elif "income" in query or "salary" in query or "earn" in query:
        st.info(f"📊 **Data Analysis Readout:** Your comprehensive total tracked income records show an aggregate influx of **{symbol}{total_income:,.2f}**.")
        answered = True

    elif "save" in query or "savings" in query or "leftover" in query:
        st.info(f"📊 **Data Analysis Readout:** After accounting for your total expenses, your current liquid unallocated baseline savings balance stands at **{symbol}{net_savings_liquid:,.2f}**.")
        answered = True

    # --------------------------------------------------------------------------
    # CRITERIA 2: INTENT IDENTIFICATION - THEORETICAL FINANCIAL EDUCATION RULES
    # --------------------------------------------------------------------------
    if not answered:
        KNOWLEDGE_DATA = {
            "emergency fund": "💡 **General Wealth Strategy:** An emergency reserve represents 3-6 months of necessary living variables archived cleanly inside liquid safe vehicles like High-Yield Savings Accounts.",
            "investing": "💡 **General Wealth Strategy:** Wealth building focuses heavily on dollar-cost averaging configurations targeting broad, low-cost index fund ETFs. Avoid high friction day-trading.",
            "inflation": "💡 **General Wealth Strategy:** Inflation continuously devalues dormant fiat balances. Allocating capital into compounding equities shields underlying asset purchasing power over long horizons.",
            "credit score": "💡 **General Wealth Strategy:** Optimize credit evaluations by setting automated repayment alerts and maintaining revolving line utilization metrics safely underneath 30% thresholds."
        }
        
        for keyword, analysis in KNOWLEDGE_DATA.items():
            if keyword in query:
                st.info(analysis)
                answered = True
                break
                
    # --------------------------------------------------------------------------
    # CRITERIA 3: INTENT IDENTIFICATION - FALLBACK ADVISORY ROUTING
    # --------------------------------------------------------------------------
    if not answered:
        st.warning("🤖 **System Routing Notice:** I was unable to parse that exact data command. Try framing questions around your data metrics like *'What is my highest expense?'*, *'How much did I spend on Groceries?'*, or look up core general concepts such as *'emergency fund'*.")
