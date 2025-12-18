import os

# absolute path to project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# path to Chinook sample database
DB_PATH = os.path.join(BASE_DIR, "database", "chinook.db")

# LLM model identifier
MODEL_NAME = "llama-3.3-70b-versatile"

# blocked SQL keywords
BLOCKED_KEYWORDS = ['DROP', 'TRUNCATE', 'ALTER', 'CREATE', 'PRAGMA', 'ATTACH']
