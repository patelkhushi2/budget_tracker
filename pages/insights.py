import sqlite3
import pandas as pd
import streamlit as st

conn = sqlite3.connect('budget.db') # connects to the budget database

st.set_page_config(
    page_title="Budget Tracker Insights",
    layout="wide"
)

st.title("Budget Tracker Insights")


month_filter = st.selectbox(
    "Month",
    ["August 2026", "July 2026"]
)

if month_filter == "August 2026":
    selected_month = "2026-08"
elif month_filter == "July 2026":
    selected_month = "2026-07"
    


left, right = st.columns(2)

with left:
    st.subheader("Top 5 Merchants")
    
    top5_query = """
        SELECT merchant, COUNT(*) AS transaction_count, SUM(amount) AS total_spent
        FROM transactions
        WHERE strftime('%Y-%m', transaction_date) = ? and transaction_type = 'Purchase'
        GROUP BY merchant
        ORDER BY transaction_count DESC
        LIMIT 5
    """

    st.dataframe(
        pd.read_sql_query(
            top5_query, 
            conn, 
            params=[selected_month]
        ),
        hide_index=True
    )

with right:
    st.subheader("Top 5 Categories")
    top5_categories_query = """
        SELECT categories.category_name AS Category, COUNT(*) AS transaction_count, SUM(transactions.amount) AS total_spent
        FROM transactions
        JOIN categories ON transactions.category_id = categories.category_id
        WHERE strftime('%Y-%m', transaction_date) = ? and transaction_type = 'Purchase'
        GROUP BY categories.category_name
        ORDER BY transaction_count DESC
        LIMIT 5
    """
    st.dataframe(
        pd.read_sql_query(
            top5_categories_query, 
            conn, 
            params=[selected_month]
        ),
        hide_index=True
    )
    
avg_query = """
    SELECT merchant, AVG(amount) AS average_transaction_amount
    FROM transactions
    JOIN categories ON transactions.category_id = categories.category_id
    WHERE strftime('%Y-%m', transaction_date) = ? 
        AND transaction_type = 'Purchase'
    GROUP BY merchant
    """
st.subheader("Average Transaction Amount")
avg_df = pd.read_sql_query(avg_query, conn, params=[selected_month])

st.dataframe(avg_df, hide_index=True)
