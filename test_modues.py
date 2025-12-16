from modules.schema import get_database_text
from modules.validator import validate_query
from modules.executor import execute_query

print("=== EXECUTOR TESTS ===\n")

# Test 1: Valid query with results
print("Test 1: Valid SELECT")
success, result = execute_query("SELECT * FROM Customer LIMIT 3")
if success:
    print("✅ SUCCESS")
    print(result)
else:
    print("❌ FAILED:", result)

print("\n" + "="*50 + "\n")

# Test 2: Query with no results
print("Test 2: Query with no results")
success, result = execute_query(
    "SELECT * FROM Customer WHERE CustomerId = 99999")
if success:
    print("✅ SUCCESS")
    print(result)
else:
    print("❌ FAILED:", result)

print("\n" + "="*50 + "\n")

# Test 3: Invalid query (syntax error)
print("Test 3: Invalid SQL syntax")
success, result = execute_query("SELCT * FROM Customer")
if success:
    print("✅ SUCCESS")
    print(result)
else:
    print("❌ FAILED:", result)
