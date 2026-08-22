import sqlite3
import pandas as pd
import streamlit as st

conn = sqlite3.connect('budget.db') # connects to the budget database

st.set_page_config(
    page_title="Budget Tracker",
    page_icon="💰"
)

st.title("Database Overview")

    
st.subheader("Users")

users_query = """
    SELECT *
    FROM users
    GROUP BY user_id
"""

users_df = pd.read_sql_query(users_query, conn) # executes the query and returns a dataframe

st.write(users_df)

st.subheader("Accounts")

accounts_query = """
    SELECT *
    FROM accounts
    GROUP BY account_id
"""
accounts_df = pd.read_sql_query(accounts_query, conn) # executes the query and returns a

st.write(accounts_df)

st.subheader("Categories")

category_query = """
    SELECT *
    FROM categories
    GROUP BY category_id
"""

category_df = pd.read_sql_query(category_query, conn) # executes the query and returns a dataframe

st.write(category_df)

st.subheader("Budgets")

budget_query = """
    SELECT *
    FROM budgets
    GROUP BY budget_id
"""
budget_df = pd.read_sql_query(budget_query, conn) # executes the query and returns a dataframe

st.write(budget_df)

st.subheader("Transactions")

transaction_query = """
    SELECT *
    FROM transactions
    GROUP BY transaction_id
"""

transaction_df = pd.read_sql_query(transaction_query, conn) # executes the query and returns a dataframe
st.write(transaction_df)

