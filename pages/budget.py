import sqlite3
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Budgets",
    layout="wide"
)

conn = sqlite3.connect('budget.db') # connects to the budget database

st.title("Budgets")

month_filter = st.selectbox(
    "Month",
    ["August 2026", "July 2026"]
)

if month_filter == "August 2026":
    selected_month = "2026-08"
elif month_filter == "July 2026":
    selected_month = "2026-07"
    
budget_query = """
    SELECT 
        categories.category_name AS Category, 
        budgets.budget_amount AS Budget, 
        COALESCE(SUM(transactions.amount), 0) AS Spent,
        budgets.budget_amount - COALESCE(SUM(transactions.amount), 0) AS Remaining,
        (COALESCE(SUM(transactions.amount), 0) / budgets.budget_amount) * 100 AS Percent_Spent
    FROM budgets
    JOIN categories
        ON budgets.category_id = categories.category_id
    LEFT JOIN transactions 
        ON budgets.category_id = transactions.category_id
        AND budgets.month = strftime('%Y-%m', transactions.transaction_date)
        AND transactions.transaction_type = 'Purchase'
    WHERE budgets.month = ?
        
    GROUP BY categories.category_name, budgets.budget_amount
    """

budget_df = pd.read_sql_query(
    budget_query, 
    conn, 
    params=[selected_month]
)

st.subheader("Budget Overview")
#displays the budget query result
st.bar_chart(
    budget_df,
    x="Category",
    y=["Budget", "Spent"]
)
st.dataframe(budget_df[["Category", "Budget", "Spent"]], hide_index=True,)