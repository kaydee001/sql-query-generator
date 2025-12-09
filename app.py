import streamlit as st
import sqlite3
import pandas as pd

st.title("SQL Query Generator")
sql_query = st.text_area("Enter SQL query", "SELECT * FROM customers")

with st.expander("View database : "):
    conn = sqlite3.connect("database/sales.db")
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()

    for table in tables:
        table_name = table[0]
        st.subheader(f"Table : {table_name}")

        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()

        for col in columns:
            st.text(f"  • {col[1]} ({col[2]})")

    conn.close()

if st.button("Run Query"):
    conn = sqlite3.connect("database/sales.db")
    cursor = conn.cursor()

    try:
        cursor.execute(sql_query)

        if cursor.description:
            results = cursor.fetchall()
            columns = [description[0] for description in cursor.description]
            df = pd.DataFrame(results, columns=columns)
            st.dataframe(df)
        else:
            conn.commit()
            st.success(f"Query executed - {cursor.rowcount} row(s) affected")
            st.balloons()

    except Exception as e:
        st.error(f"Error : {e}")

    finally:
        conn.close()
