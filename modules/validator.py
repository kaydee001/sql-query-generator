from .config import BLOCKED_KEYWORDS


def validate_query(sql_query: str) -> tuple[bool, str | None]:
    """
    validates the generated SQL query
    enforces read only SELECT queries and blocks dangerous operations
    """
    # normalize query for consistent validation
    query_upper = sql_query.strip().upper()

    # remove SQL comments
    query_upper = query_upper.split("--")[0].strip()

    if not query_upper:
        return False, "⚠️ Empty queries are not allowed"

    # allow only SELECT queries
    if not query_upper.startswith("SELECT"):
        return False, "⚠️ Only SELECT queries are allowed. No DML and DDL commands"

    # blocking dangerous operations
    dangerous_keywords = BLOCKED_KEYWORDS
    for keyword in dangerous_keywords:
        if keyword in query_upper:
            return False, f"⚠️ {keyword} commands are not allowed for safety reasons"

    # disallow multiple SQL statements
    if ';' in query_upper:
        return False, f"⚠️ Multiple SQL statements are not allowed"

    return True, None
