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

overview, transactions = st.columns(2)

with overview:
    st.subheader("Overview")

    #total amount of pending 
    pending_query = """
        SELECT SUM(amount) AS pending_total
        FROM transactions 
        WHERE status = 'Pending' AND transaction_type = 'Purchase'
    """

    pending_df = pd.read_sql_query(pending_query, conn) 
    pending_spending = pending_df["pending_total"].iloc[0] 

    #total amount of posted
    posted_query = """
        SELECT SUM(amount) AS posted_total
        FROM transactions 
        WHERE status = 'Posted' AND transaction_type = 'Purchase'
    """

    posted_df = pd.read_sql_query(posted_query, conn)
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



with transactions:
    st.subheader("Transactions")

    #display
    status_filter, order_filter = st.columns(2)

    with status_filter:
        status_filter = st.selectbox("Filter by Status", [
            "All", "Pending", "Posted"])
    
    with order_filter:
        order_by = st.selectbox("Order by", [
            "Oldest to Newest", "Newest to Oldest"])

    query = """
        SELECT transaction_date, merchant, amount, status
        FROM transactions
    """    
    
    if status_filter == "Pending":
        query += "WHERE status = 'Pending' "
    elif status_filter == "Posted":
        query += "WHERE status = 'Posted' "
    
    if order_by == "Oldest to Newest":
        query += "ORDER BY transaction_date ASC"
    else:
        query += "ORDER BY transaction_date DESC"
    
    df = pd.read_sql_query(query, conn) # executes the query and returns a dataframe
    st.dataframe(df, hide_index=True) # displays the dataframe in the web app without the index