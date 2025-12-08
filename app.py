import streamlit as st
import sqlite3
import pandas as pd

st.title("SQL Query Generator")
if st.button("run sample query"):
    conn = sqlite3.connect("database/sales.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM customers")
    results = cursor.fetchall()

    df = pd.DataFrame(results, columns=['id', 'name', 'email', 'total_spent'])
    st.dataframe(df)

    conn.close()