import sqlite3
import pandas as pd
from .config import DB_PATH


def execute_query(sql_query: str) -> tuple[bool, pd.DataFrame | str]:
    """
    validating SQL query
    returns results or message
    """
    try:
        # safety check : executer only runs SELECT queries
        if not sql_query.strip().upper().startswith("SELECT"):
            return False, "Only SELECT queries can be executed"

        # using pandas to execute SQL and load results directly into a DataFrame
        with sqlite3.connect(DB_PATH) as conn:
            df = pd.read_sql_query(sql_query, conn)

            # if query executes but returns no rows
            if df.empty:
                return True, "No results found"

        return True, df

    # catching database related errors
    except sqlite3.Error as e:
        return False, f"Database error : {str(e)}"

    # catching any unexpected runtime errors
    except Exception as e:
        return False, f"Unexpected error : {str(e)}"
