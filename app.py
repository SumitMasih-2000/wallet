import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# 1. Page Configuration
st.set_page_config(
    page_title="AI Personal Finance Assistant",
    page_icon="💼",
    layout="wide"
)

# Load Material Icons and Executive Dark Theme Stylesheet
st.html("""
    <link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons">
    <style>
    /* Corporate Slate Dark Canvas Base */
    .stApp { 
        background-color: #0F172A !important; 
        color: #F8FAFC !important;
    }
    
    h1, h2, h3, h4, h5, h6, label, p, .stMarkdown {
        color: #F8FAFC !important;
    }
    
    /* Segment Blocks with Rich Background Colors */
    .section-container {
        background-color: #1E293B;
        padding: 26px;
        border-radius: 12px;
        border: 1px solid #334155;
        margin-bottom: 24px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    }
    
    /* Structured Metric Display Modules */
    .metric-card {
        background-color: #334155;
        padding: 20px;
        border-radius: 8px;
        border-left: 5px solid #64748B;
        margin-bottom: 10px;
    }
    
    .metric-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 6px;
    }
    
    .metric-label { 
        color: #94A3B8; 
        font-size: 13px; 
        font-weight: 600; 
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .metric-data { 
        font-size: 28px; 
        font-weight: 700; 
        letter-spacing: -0.5px;
    }
    
    /* Status Indicator Colors */
    .border-inflow { border-left-color: #10B981 !important; }
    .border-outflow { border-left-color: #EF4444 !important; }
    .border-net { border-left-color: #3B82F6 !important; }
    .border-valuation { border-left-color: #F59E0B !important; }
    
    .text-inflow { color: #34D399; }
    .text-outflow { color: #F87171; }
    .text-net { color: #60A5FA; }
    .text-valuation { color: #FBBF24; }
    </style>
""")

# Initialize master transaction dataset
if "transactions" not in st.session_state:
    st.session_state.transactions = pd.DataFrame([
        {"Date": "2026-06-10", "Category": "Salary", "Amount": 150000.00, "Notes": "Monthly paycheck"},
        {"Date": "2026-06-12", "Category": "Rent/Utilities", "Amount": -45000.00, "Notes": "Apartment rent"},
        {"Date": "2026-06-13", "Category": "Groceries", "Amount": -12000.00, "Notes": "Grocery store run"},
        {"Date": "2026-06-14", "Category": "Dining Out", "Amount": -8500.00, "Notes": "Client business lunch"},
        {"Date": "2026-06-15", "Category": "Entertainment", "Amount": -5000.00, "Notes": "Subscription renewals"},
        {"Date": "2026-06-16", "Category": "Investments", "Amount": -20000.00, "Notes": "Index fund deposit"}
    ])

# ==============================================================================
# SIDEBAR CONTROL PANELS
# ==============================================================================
st.sidebar.markdown("### :material/tune: Control Panel")

# Currency selector configuration
currency_options = {"INR (₹)": "₹", "USD ($)": "$", "EUR (€)": "€", "GBP (£)": "£"}
selected_currency_label = st.sidebar.selectbox("Reporting Currency", options=list(currency_options.keys()), index=0)
symbol = currency_options[selected_currency_label]

# Income baseline position directly beneath currency selection configuration
income_base_input = st.sidebar.number_input(
    f"Baseline Income Reference ({symbol})", 
    min_value=100.0, 
    value=150000.0, 
    step=5000.0,
    help="Define your primary monthly base income to compute target budget distribution metrics."
)

st.sidebar.divider()
st.sidebar.markdown("### :material/filter_alt: Data Filters")

# Extraction filters
available_categories = st.session_state.transactions['Category'].unique().tolist()
selected_filters = st.sidebar.multiselect(
    "Filter Categories",
    options=available_categories,
    default=available_categories,
    help="Toggle selections to re-calculate current workspace metrics instantly."
)

# Apply global query filtering rules
df_filtered = st.session_state.transactions[st.session_state.transactions['Category'].isin(selected_filters)].copy()

# ==============================================================================
# MAIN SHEET APPLICATION HEADER
# ==============================================================================
st.title("💼 AI Personal Finance Assistant")
st.markdown("<p style='color: #94A3B8; font-size: 15px;'>Professional Portfolio Tracking & Automated Financial Analysis Engine</p>", unsafe_allow_html=True)
st.write("---")

# ==============================================================================
# ROW 1: CORE BALANCES & KPI REPORTING
# ==============================================================================
calc_income = df_filtered[df_filtered['Amount'] > 0]['Amount'].sum()
calc_expenses = abs(df_filtered[df_filtered['Amount'] < 0]['Amount'].sum())
calc_savings = calc_income - calc_expenses
mock_assets = 2500000.00
calc_networth = calc_savings + mock_assets

kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)

with kpi_col1:
    st.html(f"""
        <div class="metric-card border-inflow">
            <div class="metric-row">
                <div class="metric-label">Total Inflow</div>
                <span class="material-icons text-inflow">trending_up</span>
            </div>
            <div class="metric-data text-inflow">{symbol}{calc_income:,.2f}</div>
        </div>
    """)
with kpi_col2:
    st.html(f"""
        <div class="metric-card border-outflow">
            <div class="metric-row">
                <div class="metric-label">Total Outflow</div>
                <span class="material-icons text-outflow">trending_down</span>
            </div>
            <div class="metric-data text-outflow">{symbol}{calc_expenses:,.2f}</div>
        </div>
    """)
with kpi_col3:
    st.html(f"""
        <div class="metric-card border-net">
            <div class="metric-row">
                <div class="metric-label">Net Surplus</div>
                <span class="material-icons text-net">account_balance_wallet</span>
            </div>
            <div class="metric-data text-net">{symbol}{calc_savings:,.2f}</div>
        </div>
    """)
with kpi_col4:
    st.html(f"""
        <div class="metric-card border-valuation">
            <div class="metric-row">
                <div class="metric-label">Net Worth Estimate</div>
                <span class="material-icons text-valuation">assessment</span>
            </div>
            <div class="metric-data text-valuation">{symbol}{calc_networth:,.2f}</div>
        </div>
    """)

# ==============================================================================
# ROW 2: PRIMARY INTERACTION SUITE - AI CHAT ASSISTANT
# ==============================================================================
st.html("<div class='section-container'>")
st.markdown("##### :material/forum: AI Personal Finance Assistant Chat")
st.caption("Submit queries against active database records or request general financial planning assistance below.")

search_input = st.text_input(
    "Ask a financial question...",
    placeholder="e.g., 'What was my highest expense?', 'How much did I spend on food?', 'What is an emergency fund?'"
)

df_debts = df_filtered[df_filtered['Amount'] < 0]

if search_input:
    query = search_input.lower().strip()
    answered = False
    
    if "highest" in query or "biggest" in query or "largest" in query or "max" in query:
        if not df_debts.empty:
            max_row = df_debts.loc[abs(df_debts['Amount']).idxmax()]
            st.info(f"📊 **AI Assistant Response:** The single highest recorded expenditure matching your active filters is for **{max_row['Category']}** totaling **{symbol}{abs(max_row['Amount']):,.2f}** ({max_row['Notes']}) on {max_row['Date']}.")
        else:
            st.info("📊 **AI Assistant Response:** No negative transaction flows match your specified category layout.")
        answered = True

    elif "spend" in query or "expense" in query or "cost" in query or "total out" in query or "food" in query:
        category_mapping = {"food": "Dining Out", "groceries": "Groceries", "salary": "Salary", "rent": "Rent/Utilities"}
        
        matched_category = None
        for keyword, actual_cat in category_mapping.items():
            if keyword in query:
                matched_category = actual_cat
                break
        
        if not matched_category:
            for cat in df_filtered['Category'].unique():
                if cat.lower() in query:
                    matched_category = cat
                    break
                
        if matched_category:
            cat_sum = abs(df_filtered[df_filtered['Category'] == matched_category]['Amount'].sum())
            st.info(f"📊 **AI Assistant Response:** Total tracking expenses allocated toward **{matched_category}** aggregate to **{symbol}{cat_sum:,.2f}** under current filters.")
        else:
            st.info(f"📊 **AI Assistant Response:** Aggregate expenditures spanning all active filtration matrices match **{symbol}{calc_expenses:,.2f}**.")
        answered = True

    elif "income" in query or "salary" in query or "earn" in query:
        st.info(f"📊 **AI Assistant Response:** Total tracked income in this viewing profile is **{symbol}{calc_income:,.2f}**.")
        answered = True

    elif "save" in query or "savings" in query or "surplus" in query:
        st.info(f"📊 **AI Assistant Response:** Based on your operational variables, your net dynamic liquid surplus evaluates to **{symbol}{calc_savings:,.2f}**.")
        answered = True

    if not answered:
        KNOWLEDGE_DATA = {
            "emergency fund": "💡 **Financial Directive:** An emergency reserve consists of 3-6 months of necessary operating capital maintained in highly liquid instruments (such as an HYSA) to defend against unexpected operational disruption.",
            "investing": "💡 **Financial Directive:** Systematically compound long-term asset bases via programmatic dollar-cost averaging into low-fee diversified tracking indices, ignoring brief volatility spikes.",
            "inflation": "💡 **Financial Directive:** Cash accounts steadily lose buying power to inflationary decay. Deploying residual liquidity into productive market assets preserves purchasing power benchmarks.",
            "credit score": "💡 **Financial Directive:** Ensure flawless account status evaluations by leveraging automation structures to keep individual lines revolving below a 30% total balance utilization limit."
        }
        
        for keyword, analysis in KNOWLEDGE_DATA.items():
            if keyword in query:
                st.info(analysis)
                answered = True
                break
                
    if not answered:
        st.warning("⚠️ **AI Assistant Response:** Could not extract a precise analytical outcome matching your prompt parameters. Please verify your query or focus on dataset metrics like: *'What was my highest expense?'* or structural concepts like *'inflation'*.")

st.html("</div>")

# ==============================================================================
# ROW 3: DISTRIBUTION CHARTS & EXPENDITURE BUDGET MATRICES
# ==============================================================================
st.html("<div class='section-container'>")

chart_col_left, target_col_right = st.columns([5, 4], gap="large")

with chart_col_left:
    st.markdown("##### :material/pie_chart: Expense Distribution Analysis")
    
    df_only_expenses = df_filtered[df_filtered['Amount'] < 0].copy()
    df_only_expenses['Amount'] = abs(df_only_expenses['Amount'])
    
    if not df_only_expenses.empty:
        df_chart_grouped = df_only_expenses.groupby('Category', as_index=False)['Amount'].sum()
        
        corporate_palette = ['#3B82F6', '#EF4444', '#F59E0B', '#10B981', '#8B5CF6', '#EC4899']
        
        fig_donut = go.Figure(data=[go.Pie(
            labels=df_chart_grouped['Category'],
            values=df_chart_grouped['Amount'],
            hole=.55,
            marker=dict(colors=corporate_palette, line=dict(color='#1E293B', width=2)),
            hoverinfo='label+value+percent',
            textinfo='percent',
            textfont=dict(size=12, color='#F8FAFC')
        )])
        
        fig_donut.update_layout(
            margin=dict(t=10, b=10, l=10, r=10),
            height=260,
            showlegend=True,
            legend=dict(font=dict(color='#94A3B8'), orientation="v", y=0.5),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_donut, use_container_width=True)
    else:
        st.info("No active expenditures found matching the specified filtering metrics.")

with target_col_right:
    st.markdown("##### :material/ads_click: Balanced 50/30/20 Budget Parameters")
    
    # Target calculations use sidebar reference input value directly
    target_needs = income_base_input * 0.50
    target_wants = income_base_input * 0.30
    target_savings = income_base_input * 0.20
    
    st.html(f"""
        <div style="margin-top:14px;">
            <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
                <span style="color:#60A5FA; font-size:13px; font-weight:600;">Fixed Needs Target Allocation (50%)</span>
                <span style="color:#60A5FA; font-size:13px; font-weight:600;">{symbol}{target_needs:,.0f}</span>
            </div>
            <div style="background-color:rgba(255,255,255,0.08); height:8px; border-radius:4px; margin-bottom:18px;">
                <div style="background-color:#3B82F6; width:50%; height:100%; border-radius:4px;"></div>
            </div>
            
            <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
                <span style="color:#FBBF24; font-size:13px; font-weight:600;">Flexible Wants Target Allocation (30%)</span>
                <span style="color:#FBBF24; font-size:13px; font-weight:600;">{symbol}{target_wants:,.0f}</span>
            </div>
            <div style="background-color:rgba(255,255,255,0.08); height:8px; border-radius:4px; margin-bottom:18px;">
                <div style="background-color:#F59E0B; width:30%; height:100%; border-radius:4px;"></div>
            </div>
            
            <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
                <span style="color:#34D399; font-size:13px; font-weight:600;">Savings / Financial Investment (20%)</span>
                <span style="color:#34D399; font-size:13px; font-weight:600;">{symbol}{target_savings:,.0f}</span>
            </div>
            <div style="background-color:rgba(255,255,255,0.08); height:8px; border-radius:4px;">
                <div style="background-color:#10B981; width:20%; height:100%; border-radius:4px;"></div>
            </div>
        </div>
    """)

st.html("</div>")

# ==============================================================================
# ROW 4: HISTORICAL ASSET VALUATION & NET WORTH TREND
# ==============================================================================
st.html("<div class='section-container'>")
st.markdown("##### :material/timeline: Portfolio Capital Growth Trajectory")

if not df_filtered.empty:
    df_sorted_dates = df_filtered.copy().sort_values(by="Date")
    df_sorted_dates['Cumulative_Surplus'] = df_sorted_dates['Amount'].cumsum()
    df_sorted_dates['Net_Worth_Timeline'] = mock_assets + df_sorted_dates['Cumulative_Surplus']
    
    fig_trend = go.Figure()
    
    fig_trend.add_trace(go.Scatter(
        x=df_sorted_dates['Date'],
        y=df_sorted_dates['Cumulative_Surplus'],
        mode='lines+markers',
        name='Liquid Reserve Growth',
        fill='tozeroy',
        fillcolor='rgba(59, 130, 246, 0.1)',
        line=dict(color='#3B82F6', width=3)
    ))
    
    fig_trend.add_trace(go.Scatter(
        x=df_sorted_dates['Date'],
        y=df_sorted_dates['Net_Worth_Timeline'],
        mode='lines+markers',
        name='Aggregated Net Worth Value',
        line=dict(color='#F59E0B', width=4, dash='dash')
    ))
    
    fig_trend.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=20, b=20, l=10, r=10),
        height=280,
        legend=dict(font=dict(color='#94A3B8'), orientation="h", y=1.1, x=0),
        xaxis=dict(gridcolor='#334155', tickfont=dict(color='#94A3B8'), showgrid=True),
        yaxis=dict(gridcolor='#334155', tickfont=dict(color='#94A3B8'), showgrid=True)
    )
    st.plotly_chart(fig_trend, use_container_width=True)
else:
    st.info("Insufficient data segments found to calculate valuation timelines.")

st.html("</div>")

# ==============================================================================
# ROW 5: TRANSACTION DATA LEDGER WIDGET
# ==============================================================================
st.html("<div class='section-container'>")
st.markdown("##### :material/list_alt: Core Transaction History Ledger")

with st.expander("➕ Register New Ledger Entry", expanded=False):
    with st.form("ledger_form", clear_on_submit=True):
        col_form1, col_form2, col_form3 = st.columns(3)
        with col_form1:
            f_date = st.date_input("Date", datetime.now())
            f_cat = st.selectbox("Category", ["Salary", "Groceries", "Dining Out", "Rent/Utilities", "Entertainment", "Investments", "Other"])
        with col_form2:
            f_amt = st.number_input(f"Amount ({symbol})", value=0.0, step=500.0, help="Input standard expenses with a negative sign prefix.")
        with col_form3:
            f_note = st.text_input("Transaction Description / Notes")
            
        if st.form_submit_button("Commit Transaction Entry"):
            new_txn = {"Date": str(f_date), "Category": f_cat, "Amount": f_amt, "Notes": f_note}
            st.session_state.transactions = pd.concat([st.session_state.transactions, pd.DataFrame([new_txn])], ignore_index=True)
            st.rerun()

display_df = df_filtered.copy()
display_df = display_df.sort_values(by="Date", ascending=False)
display_df['Amount'] = display_df['Amount'].map(lambda x: f"🟢 {symbol}{x:,.2f}" if x >= 0 else f"🔴 -{symbol}{abs(x):,.2f}")

st.dataframe(display_df, use_container_width=True, hide_index=True)
st.html("</div>")
