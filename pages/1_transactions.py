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
    merchant_filter = st.selectbox("Filter by Merchant", [
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
    SELECT transaction_date, merchant, amount, status
    FROM transactions
    WHERE strftime('%Y-%m', transaction_date) = ?
"""    
    
if status_filter == "Pending":
    query += " AND status = 'Pending' "
elif status_filter == "Posted":
    query += " AND status = 'Posted' "
    
if order_by == "Oldest to Newest":
    query += "ORDER BY transaction_date ASC"
else:
    query += "ORDER BY transaction_date DESC"
    
if merchant_filter != "All":
    query += " AND merchant = ?"
    df = pd.read_sql_query(
        query, 
        conn,
        params=[selected_month, merchant_filter]
    ) # executes the query and returns a dataframe
else:
    df = pd.read_sql_query(
        query, 
        conn,
        params=[selected_month]
    ) # executes the query and returns a dataframe
    
st.dataframe(df, hide_index=True) # displays the dataframe in the web app without the index