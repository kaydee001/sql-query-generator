import sqlite3
import pandas as pd
from .config import DB_PATH


def execute_query(sql_query: str) -> tuple[bool, pd.DataFrame | str]:
    try:
        with sqlite3.connect(DB_PATH) as conn:
            df = pd.read_sql_query(sql_query, conn)

            if df.empty:
                return True, "No results found"

        return True, df

    except sqlite3.Error as e:
        return False, f"Database error : {str(e)}"

    except Exception as e:
        return False, f"Unexpected error : {str(e)}"
