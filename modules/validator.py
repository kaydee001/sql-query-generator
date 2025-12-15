from .config import BLOCKED_KEYWORDS


def validate_query(sql_query: str) -> tuple[bool, str | None]:
    query_upper = sql_query.strip().upper()

    if not query_upper:
        return False, "⚠️ Empty queries are not allowed"

    if not query_upper.startswith("SELECT"):
        return False, "⚠️ Only SELECT queries are allowed. No DML and DDL commands"

    dangerous_keywords = BLOCKED_KEYWORDS
    for keyword in dangerous_keywords:
        if keyword in query_upper:
            return False, f"⚠️ {keyword} commands are not allowed for safety reasons"

    if ';' in query_upper:
        return False, f"⚠️ Multiple SQL statements are not allowed"

    return True, None
