import streamlit as st
from modules.service import run_nl_query
from modules.schema import get_database_text
from modules.schema import get_database_schema_structured

if "last_sample" not in st.session_state:
    st.session_state["last_sample"] = "— Select a sample question —"

SAMPLE_QUESTIONS = {
    "— Select a sample question —": "",
    "Top 5 customers by spending": "Show top 5 customers by total spending",
    "Most popular artists": "Which artists have the highest total sales?",
    "Best-selling tracks": "Show top 10 best-selling tracks",
    "Revenue by country": "Show total revenue grouped by country",
    "Monthly sales trend": "Show total sales per month"
}

st.set_page_config(
    page_title="SQL Query Generator",
    page_icon="🔍",
)

st.title("SQL Query Generator")
st.caption(
    "Connected to Chinook sample database -> (music store data: customers, invoices, artists, albums, tracks).")
st.caption("Natural language -> SQL (read only)")

st.markdown("---")

try:
    schema = get_database_schema_structured()
except RuntimeError as e:
    st.error(str(e))
    st.stop()

with st.sidebar:
    st.subheader("Database")
    st.caption("Chinook sample database")

    st.markdown("Tables : ")
    for table_name, columns in schema.items():
        with st.expander(table_name):
            for col in columns:
                st.markdown(f"- `{col["name"]}`  ({col["type"]})")

sample_choice = st.selectbox(
    "Try a sample question", options=list(SAMPLE_QUESTIONS.keys()), key="sample_select")

if sample_choice != "— Select a sample question —" and sample_choice != st.session_state["last_sample"]:
    st.session_state["user_question"] = SAMPLE_QUESTIONS[sample_choice]
    st.session_state["last_sample"] = sample_choice

st.markdown("Ask a question : ")
user_question = st.text_input(
    "What would you like to know", key="user_question", placeholder="Which artists generated the most revenue?")

run = st.button("Generate + Run query", type="primary")
if run:
    with st.spinner("Running query ..."):
        response = run_nl_query(user_question)

        if not response["success"]:
            st.error(response["error"])
        else:
            st.subheader("Generated SQL")
            st.code(response["sql"], language="sql")

            st.subheader("Results")
            st.dataframe(response["result"], use_container_width=True)
            st.caption(f"{len(response["result"])} rows returned")

st.markdown("---")
st.caption("🔒 Read-only mode : only SELECT queries are allowed")
