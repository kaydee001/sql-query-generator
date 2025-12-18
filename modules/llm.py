import os
from groq import Groq
from dotenv import load_dotenv

from .config import MODEL_NAME

load_dotenv()

# fast fail if API key is missing
if not os.getenv("GROQ_API_KEY"):
    raise RuntimeError("GROQ_API_KEY is not set")

# initializing LLM client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_sql_from_natural_language(user_question: str, schema: str) -> str:
    """
    generating SQL query from NL question
    returns SQL query string on success
    else returns "UNCLEAR QUESTION"
    """
    prompt = f"""You are an SQL expert. Given this database schema : {schema}
            User question : {user_question}
            Generate only a SELECT SQL query. Follow these rules :
            1 . Only SELECT queries - no INSERT, UPDATE, DELETE, DROP etc
            2. Use SQLite syntax
            3. Return ONLY the SQL query - no explainations, no markdown, no extra text
            4. If the question is unclear or cannot be answered with the given schema, return : "Unclear Question"
            SQL Query : """

    response = client.chat.completions.create(
        model=MODEL_NAME, messages=[{"role": "user", "content": prompt}])

    # output cleanup incase the model returns markdown
    sql_query = response.choices[0].message.content.strip()
    sql_query = sql_query.replace("```sql", "").replace("```", "").strip()

    return sql_query
