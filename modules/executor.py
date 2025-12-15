import sqlite3
import pandas as pd
from .config import DB_PATH


def execute_query(sql_query: str) -> tuple[bool, pd.DataFrame | str]:
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(sql_query)

        if cursor.description:
            results = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            df = pd.DataFrame(results, columns=columns)
            return True, df

        return True, pd.DataFrame()

    except sqlite3.Error as e:
        return False, f"Database error : {str(e)}"

    except Exception as e:
        return False, f"Unexpected error : {str(e)}"
