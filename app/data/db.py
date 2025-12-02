import sqlite3
from pathlib import Path

DB_PATH = Path("DATA") / "intelligence_platform.db"

def connect_database(db_path=DB_PATH):
    return sqlite3.connect(str(db_path))

# Test the connection
test_conn = connect_database()
print(" Database connection successful!")
print(f"Database type: {type(test_conn)}")
test_conn.close()
print(" Connection closed.")

