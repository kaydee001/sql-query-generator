from modules.schema import get_database_text
from modules.validator import validate_query

# Test schema
print("=== SCHEMA TEST ===")
schema = get_database_text()
print(f"Schema loaded: {len(schema)} characters\n")

# Test validator
print("=== VALIDATOR TESTS ===")

test_queries = [
    "SELECT * FROM Customer",
    "DROP TABLE Customer",
    "SELECT * FROM Track; DROP TABLE Track;",
    "UPDATE Customer SET Name='test'"
]

for query in test_queries:
    is_valid, error = validate_query(query)
    status = "✅ ALLOWED" if is_valid else "❌ BLOCKED"
    print(f"{status}: {query}")
    if error:
        print(f"  Reason: {error}")
    print()
