import sqlite3
from .config import DB_PATH


def get_database_text():
    """
    reads the database schema and returns in plain text for LLM based SQL generation
    """
    conn = sqlite3.connect(DB_PATH)
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
            col_name = col[1]
            col_type = col[2]
            schema_text += f" - {col_name} ({col_type}) \n"

    conn.close()
    return schema_text


def get_database_schema_structured():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()

    schema = {}

    for (table_name, ) in tables:
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()

        schema[table_name] = [{"name": col[1], "type": col[2]}
                              for col in columns]

    conn.close()
    return schema
