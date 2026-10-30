import sqlite3
from datetime import datetime

class DBManager:
    def __init__(self, db_name="fim_repository.db"):
        self.db_name = db_name
        self.init_db()

    def init_db(self):
        """Creates the baseline table if it doesn't exist."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS file_baseline (
                    filepath TEXT PRIMARY KEY,
                    filename TEXT,
                    sha256_hash TEXT,
                    last_seen TEXT,
                    file_content TEXT
                )
            """)
            conn.commit()

    def save_baseline(self, filepath, filename, sha256_hash, content):
        """Inserts or replaces file metadata into the database."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO file_baseline (filepath, filename, sha256_hash, last_seen, file_content)
                VALUES (?, ?, ?, ?, ?)
            """, (filepath, filename, sha256_hash, timestamp, content))
            conn.commit()

    def get_all_records(self):
        """Fetches all records mapped by filepath for easy memory comparisons."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT filepath, filename, sha256_hash, last_seen FROM file_baseline")
            rows = cursor.fetchall()
            
        # Correctly maps raw elements explicitly using indexed rows
        return {row[0]: {"filename": row[1], "hash": row[2], "seen": row[3]} for row in rows}

    def get_file_content(self, filepath):
        """Retrieves historical baseline content for a specific file."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT file_content FROM file_baseline WHERE filepath = ?", (filepath,))
            row = cursor.fetchone()
        
        if row:
            return row[0] if isinstance(row, tuple) else row
        return ""
