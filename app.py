import sqlite3 #stores data in a local database
import pandas as pd # handles returned data
import streamlit as st # creates a web app

conn = sqlite3.connect('budget.db') # connects to a database file called budget.db


st.title("Budget Transactions")
st.subheader("Transactions")

status_filter = st.selectbox("Filter by Status", [
    "All", "Pending", "Posted"])

if status_filter == "All":
    query = """
    SELECT transaction_date, merchant, amount, status
    FROM transactions;
    """

    df = pd.read_sql_query(query, conn)
    
if status_filter == "Pending":
    query = """
    SELECT transaction_date, merchant, amount, status
    FROM transactions
    WHERE status = 'Pending';
    """
    df = pd.read_sql_query(query, conn)

if status_filter == "Posted":
    query = """
    SELECT transaction_date, merchant, amount, status
    FROM transactions
    WHERE status = 'Posted';
    """
    df = pd.read_sql_query(query, conn) 
    
order_by = st.selectbox("Order by", [
    "Oldest to Newest", "Newest to Oldest"])

if order_by == "Oldest to Newest":
    query = """
    SELECT transaction_date, merchant, amount, status
    FROM transactions
    ORDER BY transaction_date ASC;
    """
    
if order_by == "Newest to Oldest":
    query = """
    SELECT transaction_date, merchant, amount, status
    FROM transactions
    ORDER BY transaction_date DESC;
    """
    
st.dataframe(df)