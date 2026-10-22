"""user repository module for managing users."""

from repositories.repository import BaseRepository


class UserRepository(BaseRepository):
    """Repository for creating and retrieving user records."""

    def create_table(self) -> None:
        """Create the users table if it does not already exist."""
        sql = """
        CREATE TABLE IF NOT EXISTS users (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,

        UNIQUE(name)
        )
        """
        self.execute(sql)

    def insert_user(self, name: str) -> int:
        """Insert a user or return the existing user's identifier."""
        sql = """SELECT id FROM users WHERE name = :name"""
        params = {"name": name}
        user = self.fetch_one(sql, params)

        if user:
            return user["id"]
        sql = """
        INSERT INTO users (name) VALUES (:name)
        """
        return self.execute(sql, params)

    def get_user_id(self, user_name: str) -> int:
        """Look up a user's identifier by name."""

        sql = """
        SELECT id, name FROM users WHERE name = :name LIMIT 1
        """
        params = {"name": user_name}

        row = self.fetch_one(sql, params)
        user_id = row.get("id")
        if user_id is None:
            raise ValueError(f"User not found: {user_name}")
        return int(user_id)

    def list_users(self) -> list[dict]:
        """Return all user records."""
        sql = """
        SELECT * FROM users
        """
        return self.fetch_all(sql)
