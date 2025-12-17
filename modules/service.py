from .schema import get_database_text
from .llm import generate_sql_from_natural_language
from .validator import validate_query
from .executor import execute_query


def run_nl_query(user_question: str):
    """
    runs a natural language query end to end
    NL -> SQL -> validation -> execution
    """
    # catch any empty input
    if not user_question or not user_question.strip():
        return {
            "success": False,
            "stage": "input",
            "error": "Empty question is not allowed"
        }

    # load database schema from LLM context
    schema = get_database_text()

    # generate  SQL from NL
    sql_query = generate_sql_from_natural_language(user_question, schema)

    # handling unclear/unanswerable questions from the LLM
    if sql_query == "UNCLEAR_QUESTION":
        return {
            "success": False,
            "stage": "LLM",
            "error": "The question could not be understood using the given schema"
        }

    # validate generated SQL
    is_valid, error = validate_query(sql_query)
    if not is_valid:
        return {
            "success": False,
            "stage": "validation",
            "error": error,
            "sql": sql_query,
        }

    # execute validated SQL
    success, result = execute_query(sql_query)
    if not success:
        return {
            "success": False,
            "stage": "execution",
            "error": result,
            "sql": sql_query,
        }

    return {
        "success": True,
        "sql": sql_query,
        "result": result,
    }
