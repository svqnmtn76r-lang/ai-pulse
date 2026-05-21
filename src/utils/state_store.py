import sqlite3
from pathlib import Path
from contextlib import contextmanager

DB_PATH = Path("data/seen_articles.db")


class SeenArticleStore:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_schema()

    @contextmanager
    def _conn(self):
        conn = sqlite3.connect(self.db_path)
        try:
            yield conn
        finally:
            conn.close()

    def _init_schema(self):
        with self._conn() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS seen_articles (
                    id TEXT PRIMARY KEY,
                    source TEXT NOT NULL,
                    title TEXT,
                    url TEXT,
                    seen_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()

    def exists(self, article_id: str) -> bool:
        with self._conn() as conn:
            cur = conn.execute(
                "SELECT 1 FROM seen_articles WHERE id = ?", (article_id,)
            )
            return cur.fetchone() is not None

    def mark_seen(self, article_id: str, source: str, title: str, url: str):
        with self._conn() as conn:
            conn.execute(
                "INSERT OR IGNORE INTO seen_articles (id, source, title, url) VALUES (?, ?, ?, ?)",
                (article_id, source, title, url),
            )
            conn.commit()
