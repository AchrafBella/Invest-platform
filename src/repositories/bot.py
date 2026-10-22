"""Bots repository module for managing trading bot records."""

from repositories.repository import BaseRepository


class BotRepository(BaseRepository):
    """Repository for managing trading bot records in a SQLite database.

    This class provides CRUD operations for bot configuration and metadata,
    allowing you to create, store, and retrieve bot information.
    """

    def create_table(self) -> None:
        """Create the bots table if it does not already exist.

        The table stores bot configuration with bot_type restricted to
        'AI', 'Rule-Based', or 'Hybrid' values.
        """
        sql = """
        CREATE TABLE IF NOT EXISTS bots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            creation_date DATETIME NOT NULL DEFAULT (CURRENT_TIMESTAMP),
            bot_type TEXT,

            CHECK (bot_type IN ('AI', 'Rule-Based', 'Hybrid')),
            UNIQUE (user_id, name),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
        """
        self.execute(sql)

    def insert_bot(self, user_id: int, name: str) -> int:
        """Insert a bot or return the existing bot's identifier."""
        sql = """
            SELECT id
            FROM bots
            WHERE user_id = :user_id
            AND name = :name
          """
        params = {"user_id": user_id, "name": name}
        bot = self.fetch_one(sql, params)

        if bot:
            return bot["id"]
        sql = """
        INSERT INTO bots (user_id, name)
        VALUES (:user_id, :name)
        """
        return self.execute(sql, params)

    def list_bots(self) -> list[dict]:
        """Retrieve all bot records from the database.

        Returns:
            list[dict]: List of dictionaries, each containing id, name,
                       and  of a bot.
        """
        sql = """
        SELECT id, user_id, name
        FROM BOTS
        """
        return self.fetch_all(sql)
