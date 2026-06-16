import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# 1. Page Configuration
st.set_page_config(
    page_title="Aegis AI Personal Finance Assistant",
    page_icon="🪄",
    layout="wide"
)

# Load Material Icons and Premium Stylesheet
st.html("""
    <link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons">
    <style>
    /* Premium Dark Core */
    .stApp { 
        background-color: #0B0F19 !important; 
        color: #F1F5F9 !important;
    }
    
    h1, h2, h3, h4, h5, h6, label, p, .stMarkdown {
        color: #F1F5F9 !important;
    }
    
    /* Sleek Frosted Glass Cards */
    .kpi-card {
        background: rgba(30, 41, 59, 0.4);
        backdrop-filter: blur(8px);
        padding: 22px;
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        margin-bottom: 15px;
        transition: transform 0.2s ease;
    }
    
    .kpi-title-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 8px;
    }
    
    .kpi-title { 
        color: #94A3B8; 
        font-size: 13px; 
        font-weight: 600; 
        letter-spacing: 0.5px;
    }
    
    .kpi-value { 
        font-size: 30px; 
        font-weight: 700; 
        letter-spacing: -0.5px;
    }
    
    /* Cyber Accent States */
    .icon-income { color: #10B981; }
    .icon-expenses { color: #F43F5E; }
    .icon-savings { color: #3B82F6; }
    .icon-networth { color: #A855F7; }
    
    /* Glow highlights on top borders */
    .glow-income { border-top: 3px solid #10B981; }
    .glow-expenses { border-top: 3px solid #F43F5E; }
    .glow-savings { border-top: 3px solid #3B82F6; }
    .glow-networth { border-top: 3px solid #A855F7; }
    </style>
""")

# Initialize transaction data loop
if "transactions" not in st.session_state:
    st.session_state.transactions = pd.DataFrame([
        {"Date": "2026-06-10", "Category": "Salary", "Amount": 150000.00, "Notes": "Monthly paycheck"},
        {"Date": "2026-06-12", "Category": "Rent/Utilities", "Amount": -45000.00, "Notes": "Apartment rent"},
        {"Date": "2026-06-13", "Category": "Groceries", "Amount": -12000.00, "Notes": "Whole Foods run"},
        {"Date": "2026-06-14", "Category": "Dining Out", "Amount": -8500.00, "Notes": "Sushi with friends"},
        {"Date": "2026-06-15", "Category": "Entertainment", "Amount": -5000.00, "Notes": "Concert ticket"},
        {"Date": "2026-06-16", "Category": "Investments", "Amount": -20000.00, "Notes": "S&P 500 deposit"}
    ])

# ==============================================================================
# SIDEBAR CONTROL & SELECTION ENGINE (FILTERS)
# ==============================================================================
st.sidebar.markdown("### :material/tune: Settings")

# Currency Setup
currency_options = {"INR (₹)": "₹", "USD ($)": "$", "EUR (€)": "€", "GBP (£)": "£"}
selected_currency_label = st.sidebar.selectbox("Preferred Currency", options=list(currency_options.keys()), index=0)
symbol = currency_options[selected_currency_label]

st.sidebar.divider()
st.sidebar.markdown("### :material/filter_alt: Filters")

# Category multi-select filter
available_categories = st.session_state.transactions['Category'].unique().tolist()
selected_filters = st.sidebar.multiselect(
    "Include Categories",
    options=available_categories,
    default=available_categories,
    help="Toggle categories to instantly update your smart insights dashboards."
)

# Filter dataset based on selection
df_filtered = st.session_state.transactions[st.session_state.transactions['Category'].isin(selected_filters)].copy()

# ==============================================================================
# MAIN APPLICATION HEADER
# ==============================================================================
st.title("✨ Aegis AI Personal Finance Assistant")
st.markdown("<p style='color: #94A3B8; font-size: 16px;'>Your intelligent smart-money companion • Continuous transaction mapping</p>", unsafe_allow_html=True)
st.write("---")

# ==============================================================================
# ROW 1: PREMIUM KPI CARDS WITH INCORPORATED VECTOR ICONS
# ==============================================================================
calc_income = df_filtered[df_filtered['Amount'] > 0]['Amount'].sum()
calc_expenses = abs(df_filtered[df_filtered['Amount'] < 0]['Amount'].sum())
calc_savings = calc_income - calc_expenses
mock_assets = 2500000.00
calc_networth = calc_savings + mock_assets

kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)

with kpi_col1:
    st.html(f"""
        <div class="kpi-card glow-income">
            <div class="kpi-title-row">
                <div class="kpi-title">Total Inflow</div>
                <span class="material-icons icon-income">trending_up</span>
            </div>
            <div class="kpi-value" style="color: #34D399;">{symbol}{calc_income:,.2f}</div>
        </div>
    """)
with kpi_col2:
    st.html(f"""
        <div class="kpi-card glow-expenses">
            <div class="kpi-title-row">
                <div class="kpi-title">Total Spending</div>
                <span class="material-icons icon-expenses">trending_down</span>
            </div>
            <div class="kpi-value" style="color: #FB7185;">{symbol}{calc_expenses:,.2f}</div>
        </div>
    """)
with kpi_col3:
    st.html(f"""
        <div class="kpi-card glow-savings">
            <div class="kpi-title-row">
                <div class="kpi-title">Net Savings</div>
                <span class="material-icons icon-savings">wallet</span>
            </div>
            <div class="kpi-value" style="color: #60A5FA;">{symbol}{calc_savings:,.2f}</div>
        </div>
    """)
with kpi_col4:
    st.html(f"""
        <div class="kpi-card glow-networth">
            <div class="kpi-title-row">
                <div class="kpi-title">Estimated Net Worth</div>
                <span class="material-icons icon-networth">auto_awesome</span>
            </div>
            <div class="kpi-value" style="color: #C084FC;">{symbol}{calc_networth:,.2f}</div>
        </div>
    """)

# ==============================================================================
# ROW 2: CHARTS & BUDGET MATRICES
# ==============================================================================
chart_col_left, target_col_right = st.columns([5, 4], gap="large")

with chart_col_left:
    st.markdown("#### :material/donut_large: Spending Breakdown")
    
    df_only_expenses = df_filtered[df_filtered['Amount'] < 0].copy()
    df_only_expenses['Amount'] = abs(df_only_expenses['Amount'])
    
    if not df_only_expenses.empty:
        df_chart_grouped = df_only_expenses.groupby('Category', as_index=False)['Amount'].sum()
        
        # High-Saturation Dark-Mode Responsive Palette
        vibrant_colors = ['#FF007F', '#00F0FF', '#FFB300', '#A855F7', '#00FF66', '#FF5500']
        
        fig_donut = go.Figure(data=[go.Pie(
            labels=df_chart_grouped['Category'],
            values=df_chart_grouped['Amount'],
            hole=.6,
            marker=dict(colors=vibrant_colors, line=dict(color='#0B0F19', width=2)),
            hoverinfo='label+value+percent',
            textinfo='percent',
            textfont=dict(size=13, color='#F8FAFC')
        )])
        
        fig_donut.update_layout(
            margin=dict(t=10, b=10, l=10, r=10),
            height=280,
            showlegend=True,
            legend=dict(font=dict(color='#94A3B8'), orientation="v", y=0.5),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_donut, use_container_width=True)
    else:
        st.info("No expenditures match your active filters profile.")

with target_col_right:
    st.markdown("#### :material/track_changes: Smart 50/30/20 Target Tracker")
    
    income_base_input = st.number_input(f"Reference Monthly Income Baseline ({symbol})", min_value=100.0, value=150000.0, step=5000.0)
    
    target_needs = income_base_input * 0.50
    target_wants = income_base_input * 0.30
    target_savings = income_base_input * 0.20
    
    st.html(f"""
        <div style="margin-top:14px;">
            <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
                <span style="color:#00F0FF; font-size:13px; font-weight:600;">Needs Budget Target (50%)</span>
                <span style="color:#00F0FF; font-size:13px; font-weight:600;">{symbol}{target_needs:,.0f}</span>
            </div>
            <div style="background-color:rgba(255,255,255,0.1); height:8px; border-radius:4px; margin-bottom:18px;">
                <div style="background-color:#00F0FF; width:50%; height:100%; border-radius:4px;"></div>
            </div>
            
            <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
                <span style="color:#FFB300; font-size:13px; font-weight:600;">Wants Budget Target (30%)</span>
                <span style="color:#FFB300; font-size:13px; font-weight:600;">{symbol}{target_wants:,.0f}</span>
            </div>
            <div style="background-color:rgba(255,255,255,0.1); height:8px; border-radius:4px; margin-bottom:18px;">
                <div style="background-color:#FFB300; width:30%; height:100%; border-radius:4px;"></div>
            </div>
            
            <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
                <span style="color:#00FF66; font-size:13px; font-weight:600;">Savings Target (20%)</span>
                <span style="color:#00FF66; font-size:13px; font-weight:600;">{symbol}{target_savings:,.0f}</span>
            </div>
            <div style="background-color:rgba(255,255,255,0.1); height:8px; border-radius:4px;">
                <div style="background-color:#00FF66; width:20%; height:100%; border-radius:4px;"></div>
            </div>
        </div>
    """)

st.write("---")

# ==============================================================================
# ROW 3: REBRANDED TRANSACTION LEDGER
# ==============================================================================
st.markdown("#### :material/receipt_long: Transaction History Ledger")

with st.expander("➕ Log a New Transaction", expanded=False):
    with st.form("ledger_form", clear_on_submit=True):
        col_form1, col_form2, col_form3 = st.columns(3)
        with col_form1:
            f_date = st.date_input("Date", datetime.now())
            f_cat = st.selectbox("Category", ["Salary", "Groceries", "Dining Out", "Rent/Utilities", "Entertainment", "Investments", "Other"])
        with col_form2:
            f_amt = st.number_input(f"Amount ({symbol})", value=0.0, step=500.0, help="Type a negative sign prefix for outlays/expenses.")
        with col_form3:
            f_note = st.text_input("Memo / Description")
            
        if st.form_submit_button("Add Transaction"):
            new_txn = {"Date": str(f_date), "Category": f_cat, "Amount": f_amt, "Notes": f_note}
            st.session_state.transactions = pd.concat([st.session_state.transactions, pd.DataFrame([new_txn])], ignore_index=True)
            st.rerun()

# Apply active filters to ledger render
display_df = df_filtered.copy()
display_df = display_df.sort_values(by="Date", ascending=False)
display_df['Amount'] = display_df['Amount'].map(lambda x: f"➕ {symbol}{x:,.2f}" if x >= 0 else f"➖ -{symbol}{abs(x):,.2f}")

st.dataframe(display_df, use_container_width=True, hide_index=True)
st.write("---")

# ==============================================================================
# ROW 4: AI PERSONAL FINANCE CHAT ASSISTANT
# ==============================================================================
st.markdown("#### :material/psychology: AI Personal Finance Assistant Chat")
st.caption("Ask me questions regarding your transaction data history, monthly totals, or personal budget strategies.")

search_input = st.text_input(
    "Chat with your assistant...",
    placeholder="e.g., 'What was my highest expense?', 'How much did I spend on food?', 'What is an emergency fund?'"
)

df_debts = df_filtered[df_filtered['Amount'] < 0]

if search_input:
    query = search_input.lower().strip()
    answered = False
    
    if "highest" in query or "biggest" in query or "largest" in query or "max" in query:
        if not df_debts.empty:
            max_row = df_debts.loc[abs(df_debts['Amount']).idxmax()]
            st.info(f"✨ **AI Assistant:** Your largest individual expense among the filtered data points is for **{max_row['Category']}** at **{symbol}{abs(max_row['Amount']):,.2f}** ({max_row['Notes']}) on {max_row['Date']}.")
        else:
            st.info("✨ **AI Assistant:** I couldn't find any outgoing expenses matching your current filters.")
        answered = True

    elif "spend" in query or "expense" in query or "cost" in query or "total out" in query or "food" in query:
        # Map a few synonyms for smart UX matching
        category_mapping = {"food": "Dining Out", "groceries": "Groceries", "salary": "Salary", "rent": "Rent/Utilities"}
        
        matched_category = None
        for keyword, actual_cat in category_mapping.items():
            if keyword in query:
                matched_category = actual_cat
                break
        
        # If no custom synonym mapped, scan against exact names
        if not matched_category:
            for cat in df_filtered['Category'].unique():
                if cat.lower() in query:
                    matched_category = cat
                    break
                
        if matched_category:
            cat_sum = abs(df_filtered[df_filtered['Category'] == matched_category]['Amount'].sum())
            st.info(f"✨ **AI Assistant:** You have spent a total of **{symbol}{cat_sum:,.2f}** on **{matched_category}** based on your current filters.")
        else:
            st.info(f"✨ **AI Assistant:** Your total tracked spending across your active filter selections equals **{symbol}{calc_expenses:,.2f}**.")
        answered = True

    elif "income" in query or "salary" in query or "earn" in query:
        st.info(f"✨ **AI Assistant:** Your total tracked dynamic income influx stands at **{symbol}{calc_income:,.2f}**.")
        answered = True

    elif "save" in query or "savings" in query or "surplus" in query:
        st.info(f"✨ **AI Assistant:** Based on your current transaction streams, your net liquid surplus left over is **{symbol}{calc_savings:,.2f}**.")
        answered = True

    if not answered:
        KNOWLEDGE_DATA = {
            "emergency fund": "💡 **AI Financial Tip:** An emergency fund represents 3-6 months' worth of mandatory cash runway safely stored inside a high-yield storage vehicle (like an HYSA) to act as an uncorrupted margin against macro shocks.",
            "investing": "💡 **AI Financial Tip:** Building long-term wealth is most effectively realized via consistent automated index fund dollar-cost averaging. Minimize short-term noise allocations.",
            "inflation": "💡 **AI Financial Tip:** Cash loses purchasing power over time due to inflation. Shield your hard-earned value by systematically moving surplus cash into long-term compounding assets.",
            "credit score": "💡 **AI Financial Tip:** Maintain a flawless repayment loop history and keep your rolling utilization rates safely under 30% thresholds to optimize personal creditworthiness scores."
        }
        
        for keyword, analysis in KNOWLEDGE_DATA.items():
            if keyword in query:
                st.info(analysis)
                answered = True
                break
                
    if not answered:
        st.warning("🤖 **AI Assistant:** I'm not sure how to calculate that specific prompt yet! Try checking data points directly by asking things like *'What was my highest expense?'*, *'How much did I earn?'*, or ask general concepts like *'What is an emergency fund?'*")
