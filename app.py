import os
import pandas as pd
import streamlit as st
import sqlite3
from dotenv import load_dotenv
from groq import Groq

load_dotenv()


def get_database_schema():
    conn = sqlite3.connect("database/sales.db")
    cursor = conn.cursor()

    schema_text = ""

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()

    for table in tables:
        table_name = table[0]
        schema_text += f"\nTable : {table_name}\n"

        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()

        for col in columns:
            schema_text += f"- {col[1]} ({col[2]})\n"

    conn.close()
    return schema_text


def generate_sql_from_natural_language(user_question, schema):
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    prompt = f"""You are an SQL expert. Given this database schema : {schema}
    User question : "{user_question}"
    Generate ONLY SQL query; nothing else. No explainations, no markdown; just the SQL query.
    User SQLite syntax """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": prompt}])

    sql_query = response.choices[0].message.content.strip()
    sql_query = sql_query.replace("```sql", "").replace("```", "").strip()

    return sql_query


st.title("SQL Query Generator")

with st.expander("View Database Schema : "):
    conn = sqlite3.connect("database/sales.db")
    cursor = conn.cursor()

    schema_text = ""

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()

    for table in tables:
        table_name = table[0]
        st.subheader(f"Table: {table_name}")

        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()

        for col in columns:
            st.text(f"  • {col[1]} ({col[2]})")

    conn.close()

mode = st.radio("Choose input mode : ", [
                "Write SQL", "Ask in natural language"])

if mode == "Write SQL":
    sql_query = st.text_area("Enter SQL query", "SELECT * FROM customers")

    if st.button("Run Query"):
        conn = sqlite3.connect("database/sales.db")
        cursor = conn.cursor()

        try:
            cursor.execute(sql_query)

            if cursor.description:
                results = cursor.fetchall()
                columns = [description[0]
                           for description in cursor.description]
                df = pd.DataFrame(results, columns=columns)
                st.dataframe(df)
            else:
                conn.commit()
                st.success(
                    f"Query executed - {cursor.rowcount} row(s) affected")
                st.balloons()

        except Exception as e:
            st.error(f"Error : {e}")

        finally:
            conn.close()

else:
    user_question = st.text_input(
        "Ask a question about your data : ", "Show me all customers")

    if st.button("Generate & Run Query : "):
        with st.spinner("Generating SQL"):
            schema = get_database_schema()

            generated_sql = generate_sql_from_natural_language(
                user_question, schema)

            st.subheader("Generated SQL : ")
            st.code(generated_sql, language="sql")

        conn = sqlite3.connect("database/sales.db")
        cursor = conn.cursor()

        try:
            cursor.execute(generated_sql)

            if cursor.description:
                results = cursor.fetchall()
                columns = [description[0]
                           for description in cursor.description]
                df = pd.DataFrame(results, columns=columns)
                st.dataframe(df)
            else:
                conn.commit()
                st.success(
                    f"Query executed - {cursor.rowcount} row(s) affected")
                st.balloons()

        except Exception as e:
            st.error(f"Error: {e}")

        finally:
            conn.close()
