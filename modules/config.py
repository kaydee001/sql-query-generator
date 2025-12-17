import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "database", "chinook.db")

MODEL_NAME = "llama-3.3-70b-versatile"

BLOCKED_KEYWORDS = ['DROP', 'TRUNCATE', 'ALTER', 'CREATE', 'PRAGMA', 'ATTACH']
