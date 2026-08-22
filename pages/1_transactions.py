import sqlite3
import pandas as pd
import streamlit as st

conn = sqlite3.connect('budget.db') # connects to the budget database

st.set_page_config(
    page_title="Transactions",
    layout="wide",
)

st.title("Transactions")


month_filter = st.selectbox(
    "Month",
    ["August 2026", "July 2026"]
)
if month_filter == "August 2026":
    selected_month = "2026-08"
elif month_filter == "July 2026":
    selected_month = "2026-07"

#display
status_filter, order_filter, category_filter = st.columns(3)

with status_filter:
    status_filter = st.selectbox("Filter by Status", [
        "All", "Pending", "Posted"])
    
with order_filter:
    order_by = st.selectbox("Order by", [
        "Oldest to Newest", 
        "Newest to Oldest"]
)

with category_filter:
    category_filter = st.selectbox("Filter by Category", [
        "All",
        "Dining",
        "Groceries",
        "Gas",
        "Entertainment",
        "Utilities",
        "Shopping",
        "Subscription",
        "Transportation",
        "Personal Care",
        "Bills",
        "Income",
        "Transfer",
])

query = """
    SELECT 
        transactions.transaction_date,
        transactions.merchant,
        categories.category_name AS category,
        transactions.amount,
        transactions.status
    FROM transactions
    JOIN categories
        ON transactions.category_id = categories.category_id
    WHERE strftime('%Y-%m', transactions.transaction_date) = ?
"""   
    
if status_filter == "Pending":
    query += " AND status = 'Pending' "
elif status_filter == "Posted":
    query += " AND status = 'Posted' "

if category_filter != "All":
    query += " AND categories.category_name = ?"

if order_by == "Oldest to Newest":
    query += " ORDER BY transaction_date ASC"
else:
    query += " ORDER BY transaction_date DESC"
    
if category_filter != "All":
    df = pd.read_sql_query(
        query, 
        conn,
        params=[selected_month, category_filter]
    ) # executes the query and returns a dataframe
else:
    df = pd.read_sql_query(
        query, 
        conn,
        params=[selected_month]
    ) # executes the query and returns a dataframe

total_col, count_col = st.columns(2)

with total_col:
    total_amount=df["amount"].sum()
    st.metric(
        label="Total",
        value=f"${total_amount:,.2f}"
    )

with count_col:
    transaction_count = len(df)
    st.metric(
        label="Transactions",
        value=transaction_count
    ) 

st.dataframe(df, hide_index=True, width="stretch") # displays the dataframe in the web app without the index