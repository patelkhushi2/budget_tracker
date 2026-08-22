import sqlite3 #stores data in a local database
import pandas as pd # handles returned data
import streamlit as st # creates a web app
st.set_page_config(
    page_title="Budget Tracker",
    layout="wide"
)


conn = sqlite3.connect('budget.db') # connects to the budget database

#title and subtitle for the web app
st.title("Budget Transactions")

month,top = st.columns([1, 3])

#month dropbox + logic
with month:
    month_filter = st.selectbox(
        "Month",
        ["August 2026", "July 2026"]
    )
    if month_filter == "August 2026":
        selected_month = "2026-08"
    elif month_filter == "July 2026":
        selected_month = "2026-07"

overview, transactions = st.columns(2)

with overview:
    st.subheader("Overview")

    #total amount of pending 
    pending_query = """
        SELECT COALESCE(SUM(amount), 0) AS pending_total
        FROM transactions 
        WHERE status = 'Pending' AND transaction_type = 'Purchase' AND strftime('%Y-%m', transaction_date) = ?
    """

    pending_df = pd.read_sql_query(pending_query, conn, params=[selected_month])
    pending_spending = pending_df["pending_total"].iloc[0]

    #total amount of posted
    posted_query = """
        SELECT COALESCE(SUM(amount), 0) AS posted_total
        FROM transactions 
        WHERE status = 'Posted' AND transaction_type = 'Purchase' AND strftime('%Y-%m', transaction_date) = ?
    """

    posted_df = pd.read_sql_query(posted_query, conn, params=[selected_month])
    posted_spending = posted_df["posted_total"].iloc[0]

    #display
    total, pending, posted = st.columns(3)

    with total:
        st.metric(
            label="Total Spending",
            value=f"${pending_spending + posted_spending:,.2f}"
        )

    with pending:
        st.metric(
            label="Pending Spending",
            value=f"${pending_spending:,.2f}"
        )

    with posted:
        st.metric(
            label="Posted Spending",
            value=f"${posted_spending:,.2f}"
        )
        
    st.subheader("Income vs Spending")
    
    income_query = """
        SELECT COALESCE(SUM(amount), 0) AS income_total
        FROM transactions 
        WHERE transaction_type = 'Income' AND strftime('%Y-%m', transaction_date) = ?
    """
    
    income_df = pd.read_sql_query(income_query, conn, params=[selected_month])
    income_total = income_df["income_total"].iloc[0]
    st.metric(
        label="Total Income",
        value=f"${income_total:,.2f}"
    )

    
    

with transactions:
    st.subheader("Transactions")
    
    number_of_transactions_query = """
        SELECT COUNT(*) AS transaction_count
        FROM transactions
        WHERE strftime('%Y-%m', transaction_date) = ? AND transaction_type = 'Purchase'
    """
    
    transaction_count_df = pd.read_sql_query(number_of_transactions_query, conn, params=[selected_month])
    transaction_count = transaction_count_df["transaction_count"].iloc[0]

    st.write(f"Number of Transactions: {transaction_count}")

    st.subheader("Top 5 Merchants by Transaction Count")
    
    top5_query = """
        SELECT merchant, COUNT(*) AS transaction_count, SUM(amount) AS total_spent
        FROM transactions
        WHERE strftime('%Y-%m', transaction_date) = ? and transaction_type = 'Purchase'
        GROUP BY merchant
        ORDER BY transaction_count DESC
        LIMIT 5
    """
    st.dataframe(
        pd.read_sql_query(top5_query, conn, params=[selected_month]),hide_index=True
    )    