import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# 1. Page Configuration (Must be first)
st.set_page_config(
    page_title="Aegis Corporate Wealth Command",
    page_icon="📊",
    layout="wide"
)

# 2. Immersive High-Contrast Dark Command Canvas Stylesheet
st.html("""
    <style>
    /* Dark Command Viewport Foundations */
    .stApp { 
        background-color: #0F172A !important; 
        color: #F8FAFC !important;
    }
    
    /* Styling Streamlit standard text blocks for visibility */
    h1, h2, h3, h4, h5, h6, label, p, .stMarkdown {
        color: #F8FAFC !important;
    }
    
    /* Glowing Financial Indicator Blocks */
    .kpi-card {
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
        padding: 24px;
        border-radius: 14px;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
        border: 1px solid #334155;
        border-top: 5px solid #64748B;
        margin-bottom: 15px;
    }
    .kpi-title { 
        color: #94A3B8; 
        font-size: 12px; 
        font-weight: 700; 
        text-transform: uppercase; 
        letter-spacing: 1px;
    }
    .kpi-value { 
        font-size: 32px; 
        font-weight: 800; 
        margin-top: 8px;
        letter-spacing: -0.5px;
    }
    
    /* High-Vibrancy Category States */
    .kpi-income { border-top-color: #10B981 !important; color: #34D399; }
    .kpi-expenses { border-top-color: #F43F5E !important; color: #FB7185; }
    .kpi-savings { border-top-color: #3B82F6 !important; color: #60A5FA; }
    .kpi-networth { border-top-color: #F59E0B !important; color: #FBBF24; }
    
    /* Content Blocks */
    .content-card {
        background-color: #1E293B;
        padding: 24px;
        border-radius: 12px;
        border: 1px solid #334155;
        margin-bottom: 20px;
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
        {"Date": "2026-06-15", "Category": "Entertainment", "Amount": -5000.00, "Notes": "Streaming & Events"},
        {"Date": "2026-06-16", "Category": "Investments", "Amount": -20000.00, "Notes": "Index Mutual Fund Fund"}
    ])

# ==============================================================================
# SIDEBAR CONTROL & SELECTION ENGINE (FILTERS)
# ==============================================================================
st.sidebar.markdown("### 🎛️ Operations Control")

# Currency Setup
currency_options = {"INR (Ref ₹)": "₹", "USD ($)": "$", "EUR (€)": "€", "GBP (£)": "£"}
selected_currency_label = st.sidebar.selectbox("Global Currency Value Symbol", options=list(currency_options.keys()), index=0)
symbol = currency_options[selected_currency_label]

st.sidebar.divider()
st.sidebar.markdown("### 🔍 Live Data Filtering Matrix")

# Available categories for absolute sub-filtering
available_categories = st.session_state.transactions['Category'].unique().tolist()
selected_filters = st.sidebar.multiselect(
    "Isolate Flow Categories",
    options=available_categories,
    default=available_categories,
    help="Remove categories to change calculation results on charts and KPIs."
)

# Apply state filters to generate dynamic workspace views
df_filtered = st.session_state.transactions[st.session_state.transactions['Category'].isin(selected_filters)].copy()

# ==============================================================================
# HEADER SECTION
# ==============================================================================
st.title("⚡ Aegis Dashboard Analytics Platform")
st.markdown("<p style='color: #94A3B8;'>Sovereign Capital Management Engine • Real-time Transaction Ledger Metrics</p>", unsafe_allow_html=True)
st.write("---")

# ==============================================================================
# ROW 1: POWER HIGH-CONTRAST DYNAMIC KPI CARDS
# ==============================================================================
calc_income = df_filtered[df_filtered['Amount'] > 0]['Amount'].sum()
calc_expenses = abs(df_filtered[df_filtered['Amount'] < 0]['Amount'].sum())
calc_savings = calc_income - calc_expenses
mock_assets = 2500000.00
calc_networth = calc_savings + mock_assets

kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)

with kpi_col1:
    st.html(f"""
        <div class="kpi-card kpi-income">
            <div class="kpi-title">Inbound Income Stream</div>
            <div class="kpi-value">{symbol}{calc_income:,.2f}</div>
        </div>
    """)
with kpi_col2:
    st.html(f"""
        <div class="kpi-card kpi-expenses">
            <div class="kpi-title">Outbound Debit Profile</div>
            <div class="kpi-value">{symbol}{calc_expenses:,.2f}</div>
        </div>
    """)
with kpi_col3:
    st.html(f"""
        <div class="kpi-card kpi-savings">
            <div class="kpi-title">Calculated Net Surplus</div>
            <div class="kpi-value">{symbol}{calc_savings:,.2f}</div>
        </div>
    """)
with kpi_col4:
    st.html(f"""
        <div class="kpi-card kpi-networth">
            <div class="kpi-title">Global Portfolio Valuation</div>
            <div class="kpi-value">{symbol}{calc_networth:,.2f}</div>
        </div>
    """)

# ==============================================================================
# ROW 2: ADVANCED ANALYTICAL VISUALS & TARGET MATRIX
# ==============================================================================
chart_col_left, target_col_right = st.columns([5, 4], gap="large")

with chart_col_left:
    st.markdown("#### 📊 Categorized Capital Outflows Allocation")
    
    df_only_expenses = df_filtered[df_filtered['Amount'] < 0].copy()
    df_only_expenses['Amount'] = abs(df_only_expenses['Amount'])
    
    if not df_only_expenses.empty:
        df_chart_grouped = df_only_expenses.groupby('Category', as_index=False)['Amount'].sum()
        
        # High-Saturation Neon Color Palette
        neon_colors = ['#FF007F', '#00F0FF', '#FFB300', '#7000FF', '#00FF66', '#FF5500']
        
        fig_donut = go.Figure(data=[go.Pie(
            labels=df_chart_grouped['Category'],
            values=df_chart_grouped['Amount'],
            hole=.5,
            marker=dict(colors=neon_colors, line=dict(color='#1E293B', width=3)),
            hoverinfo='label+value+percent',
            textinfo='label+percent',
            textfont=dict(size=12, color='#F8FAFC')
        )])
        
        fig_donut.update_layout(
            margin=dict(t=10, b=10, l=10, r=10),
            height=300,
            showlegend=False,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_donut, use_container_width=True)
    else:
        st.info("No expenditure values match your active filter options selection.")

with target_col_right:
    st.markdown("#### 🎯 Active Tactical Capital Targets")
    
    # Reference target values using dynamic multi-color visual progress components
    income_base_input = st.number_input(f"Salary Base Benchmark Configuration ({symbol})", min_value=100.0, value=150000.0, step=5000.0)
    
    target_needs = income_base_input * 0.50
    target_wants = income_base_input * 0.30
    target_savings = income_base_input * 0.20
    
    st.html(f"""
        <div style="margin-top:12px;">
            <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
                <span style="color:#00F0FF; font-size:12px; font-weight:bold;">Essential Targets Base (50%)</span>
                <span style="color:#00F0FF; font-size:12px; font-weight:bold;">{symbol}{target_needs:,.0f}</span>
            </div>
            <div style="background-color:#334155; height:8px; border-radius:4px; margin-bottom:16px;">
                <div style="background-color:#00F0FF; width:50%; height:100%; border-radius:4px;"></div>
            </div>
            
            <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
                <span style="color:#FFB300; font-size:12px; font-weight:bold;">Lifestyle Target Allocations (30%)</span>
                <span style="color:#FFB300; font-size:12px; font-weight:bold;">{symbol}{target_wants:,.0f}</span>
            </div>
            <div style="background-color:#334155; height:8px; border-radius:4px; margin-bottom:16px;">
                <div style="background-color:#FFB300; width:30%; height:100%; border-radius:4px;"></div>
            </div>
            
            <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
                <span style="color:#00FF66; font-size:12px; font-weight:bold;">Future Compounding Target (20%)</span>
                <span style="color:#00FF66; font-size:12px; font-weight:bold;">{symbol}{target_savings:,.0f}</span>
            </div>
            <div style="background-color:#334155; height:8px; border-radius:4px;">
                <div style="background-color:#00FF66; width:20%; height:100%; border-radius:4px;"></div>
            </div>
        </div>
    """)

st.write("---")

# ==============================================================================
# ROW 3: RESTRUCTURED HIGH-CONTRAST DATA TRANSACTIONS MANAGER
# ==============================================================================
st.markdown("#### 📝 Institutional Modification Ledger Console")

with st.expander("➕ Log New Transaction Vector Input Parameters", expanded=False):
    with st.form("ledger_form", clear_on_submit=True):
        col_form1, col_form2, col_form3 = st.columns(3)
        with col_form1:
            f_date = st.date_input("Processing Date Value", datetime.now())
            f_cat = st.selectbox("Transaction Category Node", ["Salary", "Groceries", "Dining Out", "Rent/Utilities", "Entertainment", "Investments", "Other"])
        with col_form2:
            f_amt = st.number_input(f"Value Magnitude Transferred ({symbol})", value=0.0, step=500.0, help="Use negative signs for outlays.")
        with col_form3:
            f_note = st.text_input("Entity Counterparty System Notes")
            
        if st.form_submit_button("Commit Balance Log Operation"):
            new_txn = {"Date": str(f_date), "Category": f_cat, "Amount": f_amt, "Notes": f_note}
            st.session_state.transactions = pd.concat([st.session_state.transactions, pd.DataFrame([new_txn])], ignore_index=True)
            st.rerun()

# Processing colorized structural ledger outputs
display_df = df_filtered.copy()
display_df = display_df.sort_values(by="Date", ascending=False)
display_df['Amount'] = display_df['Amount'].map(lambda x: f"🟢 {symbol}{x:,.2f}" if x >= 0 else f"🔴 -{symbol}{abs(x):,.2f}")

st.dataframe(display_df, use_container_width=True, hide_index=True)
st.write("---")

# ==============================================================================
# ROW 4: DATA-DIVERSIFIED AI ANALYSIS COMPANION CONSOLE
# ==============================================================================
st.markdown("#### 🧠 Aegis Real-Time Contextual Core AI Advisor")
st.caption("The intelligent module processes context directly from your current active filter layout metrics.")

search_input = st.text_input(
    "Inquire about specific values (e.g., 'What is my highest expense?', 'What is my total income?', 'Give strategy for inflation')",
    placeholder="Send text inquiry commands down into our analytics node layer..."
)

df_debts = df_filtered[df_filtered['Amount'] < 0]

if search_input:
    query = search_input.lower().strip()
    answered = False
    
    if "highest" in query or "biggest" in query or "largest" in query or "max" in query:
        if not df_debts.empty:
            max_row = df_debts.loc[abs(df_debts['Amount']).idxmax()]
            st.info(f"💡 **AI Response Data Stream:** Your peak outward debit entry matching active criteria is **{max_row['Category']}** valued at **{symbol}{abs(max_row['Amount']):,.2f}** ({max_row['Notes']}) logged on {max_row['Date']}.")
        else:
            st.info("💡 **AI Response Data Stream:** No valid outbound ledger parameters found to verify highest expense limits.")
        answered = True

    elif "spend" in query or "expense" in query or "cost" in query or "total outflow" in query:
        matched_category = None
        for cat in df_filtered['Category'].unique():
            if cat.lower() in query:
                matched_category = cat
                break
                
        if matched_category:
            cat_sum = abs(df_filtered[df_filtered['Category'] == matched_category]['Amount'].sum())
            st.info(f"💡 **AI Response Data Stream:** Aggregate active debit profiles for **{matched_category}** evaluate to **{symbol}{cat_sum:,.2f}**.")
        else:
            st.info(f"💡 **AI Response Data Stream:** Globally filtered transaction outlays represent a current accumulation metric of **{symbol}{calc_expenses:,.2f}**.")
        answered = True

    elif "income" in query or "salary" in query or "earned" in query:
        st.info(f"💡 **AI Response Data Stream:** Monitored baseline inward cash inflows evaluate to **{symbol}{calc_income:,.2f}** under current selector filters.")
        answered = True

    elif "save" in query or "savings" in query or "surplus" in query:
        st.info(f"💡 **AI Response Data Stream:** Your calculated liquid surplus margin value from active parameters is **{symbol}{calc_savings:,.2f}**.")
        answered = True

    if not answered:
        KNOWLEDGE_DATA = {
            "emergency fund": "💡 **AI Corporate Strategy:** Protect underlying systems against volatile volatility vectors by buffering 3 to 6 months of absolute baseline operations cost inside high liquidity environments.",
            "investing": "💡 **AI Corporate Strategy:** Automate systemic balance standard increments toward diversified market capitalization vehicles to capture growth momentum parameters.",
            "inflation": "💡 **AI Corporate Strategy:** Inflation constantly degrades low velocity fiat holdings. Direct excess liquidity reserves into productive business equities to create capital appreciation hedges.",
            "credit score": "💡 **AI Corporate Strategy:** Protect your institutional credit evaluations by maintaining automated execution rules ensuring revolving debt balances remain below 30% thresholds."
        }
        
        for keyword, analysis in KNOWLEDGE_DATA.items():
            if keyword in query:
                st.info(analysis)
                answered = True
                break
                
    if not answered:
        st.warning("⚠️ **AI System Warning:** Prompt command scope unrecognized. Try targeting exact variables: *'What is my highest expense?'*, *'Total active income metrics?'*, or query concepts like *'inflation'*.")
