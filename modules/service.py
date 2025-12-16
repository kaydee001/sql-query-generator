from .schema import get_database_text
from .llm import generate_sql_from_natural_language
from .validator import validate_query
from .executor import execute_query


def run_nl_query(user_question: str):
    """
    runs a natural language query end to end
    NL -> SQL -> validation -> execution
    """
    if not user_question or not user_question.strip():
        return {
            "success": False,
            "stage": "input",
            "error": "Empty question is not allowed"
        }

    schema = get_database_text()
    sql_query = generate_sql_from_natural_language(user_question, schema)

    is_valid, error = validate_query(sql_query)
    if not is_valid:
        return {
            "success": False,
            "stage": "validation",
            "error": error,
            "sql": sql_query,
        }

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
