import os
import sqlite3
from .config import DB_PATH

# fast fail if database file is missing
if not os.path.exists(DB_PATH):
    raise RuntimeError(f"Database file not found at {DB_PATH}")


def get_database_text():
    """
    reads the database schema 
    returns a plain text representation used as a context for LLM based SQL generation
    """
    schema_text = ""

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        # fetch all table names
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()

        for (table_name, ) in tables:
            schema_text += f"\nTable : {table_name}\n"

            # fetch column metadata for each table
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()

            for col in columns:
                col_name = col[1]
                col_type = col[2]
                schema_text += f" - {col_name} ({col_type}) \n"

    return schema_text


def get_database_schema_structured():
    """
    returns the database schema as a structured dict
    mapping table names to column metadata
    """
    schema = {}

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()

        for (table_name, ) in tables:
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()

            schema[table_name] = [{"name": col[1], "type": col[2]}
                                  for col in columns]

    return schema
