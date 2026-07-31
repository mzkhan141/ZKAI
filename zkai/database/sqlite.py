"""SQLiteDatabase implementation."""

import sqlite3
from typing import Any, List, Optional
from zkai.database.base import Database
from zkai.core.logger import get_logger

logger = get_logger("database.sqlite")


class SQLiteDatabase(Database):
    """SQLite Database implementation."""

    def __init__(self, db_path: str = "zkai.db"):
        self.db_path = db_path
        self.conn: Optional[sqlite3.Connection] = None

    def connect(self) -> None:
        self.conn = sqlite3.connect(self.db_path)
        logger.info(f"Connected to SQLite database at {self.db_path}")

    def execute(self, query: str, params: Optional[tuple] = None) -> List[tuple]:
        if not self.conn:
            self.connect()
        cursor = self.conn.cursor()
        cursor.execute(query, params or ())
        self.conn.commit()
        return cursor.fetchall()

    def disconnect(self) -> None:
        if self.conn:
            self.conn.close()
            self.conn = None
