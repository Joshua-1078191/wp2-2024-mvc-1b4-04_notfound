import sqlite3
from pathlib import Path

def get_db():
    db_path = Path(__file__).parent.parent.parent / 'databases' / 'database.db'
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn
