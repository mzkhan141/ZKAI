"""DuckDBStore analytical database interface with native fallback."""

from typing import Any, List, Optional, Tuple
from zkai.core.logger import get_logger

logger = get_logger("storage.duckdb")

try:
    import duckdb
except ImportError:
    duckdb = None


class DuckDBStore:
    """Analytical OLAP query store leveraging DuckDB engine when installed."""

    def __init__(self, database_path: str = ":memory:"):
        self.database_path = database_path
        self.conn = duckdb.connect(database_path) if duckdb else None

    def execute_query(self, query: str, params: Optional[List[Any]] = None) -> List[Tuple[Any, ...]]:
        if not self.conn:
            logger.warning("DuckDB module is not installed; query execution bypassed.")
            return []
        cursor = self.conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        return cursor.fetchall()
