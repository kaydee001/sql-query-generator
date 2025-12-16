import streamlit as st
from modules.service import run_nl_query
from modules.schema import get_database_text

st.set_page_config(
    page_title="SQL Query Generator",
    page_icon="🔍",
    layout="centered"
)

left, center, right = st.columns([1, 3, 1])

with center:
    st.title("SQL Query Generator")
    st.caption(
        "Connected to Chinook sample database -> (music store data: customers, invoices, artists, albums, tracks).")
    st.caption("Natural language -> SQL (read only)")

st.markdown("---")

with st.sidebar:
    st.subheader("Database schema")
    st.caption("Tables and columns in the connected database")

    with st.expander("View full schema"):
        st.text(get_database_text())

st.markdown(
    "You can ask questions about : customers, invoices, artists, albums, tracks, and sales."
)

user_question = st.text_input(
    "Ask a question about your data : ", placeholder="eg. Show top 5 customers by spending")

if st.button("Generate + Run query", type="primary"):
    with st.spinner("Running query ..."):
        response = run_nl_query(user_question)

        if not response["success"]:
            st.error(response["error"])
        else:
            st.subheader("Generated SQL")
            st.code(response["sql"], language="sql")

            st.subheader("Results")
            st.dataframe(response["result"], use_container_width=True)
            st.caption(f"{len(response["result"])} rows affected")

st.markdown("---")
st.caption("🛡️ Only SELECT queries are allowed for safety")
