import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from database import FinanceDatabase
import plotly.express as px
import plotly.graph_objects as go

# Page configuration
st.set_page_config(
    page_title="Personal Finance Tracker",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        border-radius: 5px;
        padding: 10px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    h1 {
        color: #2c3e50;
        padding-bottom: 10px;
        border-bottom: 3px solid #4CAF50;
    }
    h2 {
        color: #34495e;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize database
@st.cache_resource
def get_database():
    return FinanceDatabase()

db = get_database()

# Predefined categories
INCOME_CATEGORIES = ["Salary", "Freelance", "Investment", "Gift", "Other Income"]
EXPENSE_CATEGORIES = ["Food", "Transport", "Shopping", "Bills", "Entertainment", 
                      "Healthcare", "Education", "Rent", "Other Expense"]

# Sidebar navigation
st.sidebar.title("💰 Finance Tracker")
st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "Navigation",
    ["📊 Dashboard", "➕ Add Transaction", "📝 View Transactions", "📈 Analytics"]
)

# Default user ID (in a real app, this would come from authentication)
USER_ID = 1

# Dashboard Page
if menu == "📊 Dashboard":
    st.title("📊 Financial Dashboard")
    st.markdown("### Overview of your finances")
    
    # Date range selector
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input(
            "Start Date",
            value=datetime.now().replace(day=1),
            key="dashboard_start"
        )
    with col2:
        end_date = st.date_input(
            "End Date",
            value=datetime.now(),
            key="dashboard_end"
        )
    
    # Get summary
    summary = db.get_summary(USER_ID, str(start_date), str(end_date))
    
    # Display metrics
    st.markdown("### 💳 Summary")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Income", f"${summary['total_income']:,.2f}", delta="Income")
    with col2:
        st.metric("Total Expenses", f"${summary['total_expense']:,.2f}", delta="Expense", delta_color="inverse")
    with col3:
        balance_color = "normal" if summary['balance'] >= 0 else "inverse"
        st.metric("Balance", f"${summary['balance']:,.2f}", delta=f"${summary['balance']:,.2f}")
    with col4:
        st.metric("Transactions", summary['transaction_count'])
    
    st.markdown("---")
    
    # Recent transactions
    st.markdown("### 📜 Recent Transactions")
    recent_transactions = db.get_transactions(USER_ID, str(start_date), str(end_date))
    
    if not recent_transactions.empty:
        # Display recent 10 transactions
        display_df = recent_transactions.head(10)[['date', 'type', 'category', 'amount', 'description']]
        display_df['amount'] = display_df['amount'].apply(lambda x: f"${x:,.2f}")
        st.dataframe(display_df, use_container_width=True, hide_index=True)
    else:
        st.info("No transactions found for the selected period.")

# Add Transaction Page
elif menu == "➕ Add Transaction":
    st.title("➕ Add New Transaction")
    st.markdown("### Record your income or expense")
    
    with st.form("transaction_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            trans_type = st.selectbox("Transaction Type", ["Income", "Expense"])
        
        with col2:
            if trans_type == "Income":
                category = st.selectbox("Category", INCOME_CATEGORIES)
            else:
                category = st.selectbox("Category", EXPENSE_CATEGORIES)
        
        col3, col4 = st.columns(2)
        
        with col3:
            amount = st.number_input("Amount ($)", min_value=0.01, step=0.01, format="%.2f")
        
        with col4:
            date = st.date_input("Date", value=datetime.now())
        
        description = st.text_area("Description (Optional)", placeholder="Add notes about this transaction...")
        
        submitted = st.form_submit_button("💾 Add Transaction")
        
        if submitted:
            if amount > 0:
                db.add_transaction(
                    USER_ID,
                    trans_type,
                    amount,
                    category,
                    str(date),
                    description
                )
                st.success(f"✅ {trans_type} of ${amount:,.2f} added successfully!")
                st.balloons()
            else:
                st.error("Please enter a valid amount.")

# View Transactions Page
elif menu == "📝 View Transactions":
    st.title("📝 Transaction History")
    st.markdown("### View and filter your transactions")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        filter_start = st.date_input(
            "Start Date",
            value=datetime.now() - timedelta(days=30),
            key="view_start"
        )
    
    with col2:
        filter_end = st.date_input(
            "End Date",
            value=datetime.now(),
            key="view_end"
        )
    
    with col3:
        all_categories = ["All"] + db.get_all_categories(USER_ID)
        filter_category = st.selectbox("Category", all_categories)
    
    # Get filtered transactions
    transactions = db.get_transactions(
        USER_ID,
        str(filter_start),
        str(filter_end),
        filter_category
    )
    
    if not transactions.empty:
        st.markdown(f"### Found {len(transactions)} transactions")
        
        # Display transactions
        display_df = transactions[['id', 'date', 'type', 'category', 'amount', 'description']]
        display_df['amount'] = display_df['amount'].apply(lambda x: f"${x:,.2f}")
        st.dataframe(display_df, use_container_width=True, hide_index=True)
        
        # Download CSV
        st.markdown("---")
        csv = transactions.to_csv(index=False)
        st.download_button(
            label="📥 Download CSV Report",
            data=csv,
            file_name=f"transactions_{filter_start}_{filter_end}.csv",
            mime="text/csv"
        )
    else:
        st.info("No transactions found for the selected filters.")

# Analytics Page
elif menu == "📈 Analytics":
    st.title("📈 Financial Analytics")
    st.markdown("### Visualize your spending patterns")
    
    # Date range for analytics
    col1, col2 = st.columns(2)
    with col1:
        analytics_start = st.date_input(
            "Start Date",
            value=datetime.now().replace(day=1),
            key="analytics_start"
        )
    with col2:
        analytics_end = st.date_input(
            "End Date",
            value=datetime.now(),
            key="analytics_end"
        )
    
    st.markdown("---")
    
    # Expense by Category - Pie Chart
    st.markdown("### 🥧 Expenses by Category")
    category_data = db.get_expense_by_category(USER_ID, str(analytics_start), str(analytics_end))
    
    if not category_data.empty:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            fig, ax = plt.subplots(figsize=(10, 6))
            colors = plt.cm.Set3(range(len(category_data)))
            ax.pie(
                category_data['amount'],
                labels=category_data['category'],
                autopct='%1.1f%%',
                startangle=90,
                colors=colors
            )
            ax.axis('equal')
            plt.title('Expense Distribution by Category', fontsize=14, fontweight='bold')
            st.pyplot(fig)
            plt.close()
        
        with col2:
            st.markdown("#### Category Breakdown")
            for _, row in category_data.iterrows():
                st.metric(row['category'], f"${row['amount']:,.2f}")
    else:
        st.info("No expense data available for the selected period.")
    
    st.markdown("---")
    
    # Income vs Expense - Line Chart
    st.markdown("### 📊 Income vs Expense Trend")
    trend_data = db.get_monthly_trend(USER_ID)
    
    if not trend_data.empty:
        # Pivot data for plotting
        trend_pivot = trend_data.pivot(index='month', columns='type', values='total').fillna(0)
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        if 'Income' in trend_pivot.columns:
            ax.plot(trend_pivot.index, trend_pivot['Income'], marker='o', 
                   linewidth=2, label='Income', color='#4CAF50')
        
        if 'Expense' in trend_pivot.columns:
            ax.plot(trend_pivot.index, trend_pivot['Expense'], marker='s', 
                   linewidth=2, label='Expense', color='#f44336')
        
        ax.set_xlabel('Month', fontsize=12, fontweight='bold')
        ax.set_ylabel('Amount ($)', fontsize=12, fontweight='bold')
        ax.set_title('Monthly Income vs Expense', fontsize=14, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
    else:
        st.info("No trend data available yet. Add more transactions to see trends.")

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("### 📌 About")
st.sidebar.info(
    "Personal Finance Tracker helps you manage your income and expenses efficiently. "
    "Track your spending, visualize trends, and make better financial decisions."
)
st.sidebar.markdown("---")

