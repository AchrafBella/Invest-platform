"""Shared database operations for repository classes."""

from collections.abc import Iterable
from typing import Any

from repositories.utils import connect_to_db


class BaseRepository:
    """Provide common SQLite operations for repositories."""

    def __init__(self, db_name: str):
        self.db_name = db_name

    def create_table(self) -> None:
        pass

    def execute(self, sql: str, params: dict[str, Any] | None = None) -> int:
        """Execute a modifying query and return affected row count."""

        with connect_to_db(self.db_name) as conn:
            cursor = conn.execute(sql, params or {})
            return cursor.lastrowid

    def fetch_one(
        self, sql: str, params: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """Execute a query and return one row as a dictionary."""

        with connect_to_db(self.db_name) as conn:
            cursor = conn.execute(sql, params or {})
            row = cursor.fetchone()

        return dict(row) if row is not None else {}

    def fetch_all(
        self, sql: str, params: dict[str, Any] | None = None
    ) -> list[dict[str, Any]]:
        """Execute a query and return all rows as dictionaries."""

        with connect_to_db(self.db_name) as conn:
            cursor = conn.execute(sql, params or {})
            rows: Iterable = cursor.fetchall()

        return [dict(row) for row in rows]
