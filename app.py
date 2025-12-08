import streamlit as st
import sqlite3
import pandas as pd

st.title("SQL Query Generator")
sql_query = st.text_area("Enter SQL query", "SELECT * FROM customers")

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
