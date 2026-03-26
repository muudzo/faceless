import sqlite3
import datetime
from pathlib import Path
from src.config import PROCESSED_DATA_DIR

DB_PATH = PROCESSED_DATA_DIR / "automator.db"

class Database:
    """
    SQLAlchemy-lite (pure sqlite3) for persistence.
    """
    def __init__(self):
        self.conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
        self.create_tables()

    def create_tables(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS uploads (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT,
                    title TEXT,
                    video_id TEXT,
                    url TEXT,
                    status TEXT
                )
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS research_cache (
                    topic TEXT PRIMARY KEY,
                    summary TEXT,
                    timestamp TEXT
                )
            """)

    def log_upload(self, title, video_id, url=None, status="success"):
        with self.conn:
            self.conn.execute(
                "INSERT INTO uploads (date, title, video_id, url, status) VALUES (?, ?, ?, ?, ?)",
                (datetime.datetime.now().isoformat(), title, video_id, url, status)
            )

    def cache_research(self, topic, summary):
        with self.conn:
            self.conn.execute(
                "INSERT OR REPLACE INTO research_cache (topic, summary, timestamp) VALUES (?, ?, ?)",
                (topic, summary, datetime.datetime.now().isoformat())
            )

    def get_research(self, topic):
        cur = self.conn.cursor()
        cur.execute("SELECT summary FROM research_cache WHERE topic = ?", (topic,))
        row = cur.fetchone()
        return row[0] if row else None

if __name__ == "__main__":
    db = Database()
    db.log_upload("Test Video", "12345")
    print("Database initialized and test log added.")
