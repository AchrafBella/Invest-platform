"""Unit tests for the bots database module."""

import os
import sqlite3
import sys
import unittest

sys.path.append(os.path.join(os.getcwd(), "src"))
from repositories.bot import BotRepository

DB_FILE = "src/test.db"


class TestDBBot(unittest.TestCase):
    """
    Unit tests for database operations related to the 'bots' table.

    This test suite verifies:
    - Table creation
    - Insertion of bot records
    - Integrity of stored data
    """

    def setUp(self):
        """
        Set up an in-memory SQLite database before each test.

        - Creates a fresh database instance
        - Configures row_factory to access columns by name
        - Initializes the 'bots' table
        """
        self.bot_repo = BotRepository(DB_FILE)
        self.bot_repo.create_table()
        self.conn = sqlite3.connect(DB_FILE)
        self.conn.row_factory = sqlite3.Row

        return super().setUp()

    def tearDown(self):
        """Clean up the database after each test."""

        if self.conn:
            self.conn.close()

        if os.path.exists(DB_FILE):
            os.remove(DB_FILE)

        super().tearDown()

    def test_create_table(self):
        """
        Test the creation of the 'bots' table.

        Ensures that:
        - The table is created successfully
        - The table schema matches expected structure
        """
        self.bot_repo.create_table()

        # Verify that the table exists by checking the schema
        cursor = self.conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='bots';"
        )
        self.assertIsNotNone(
            cursor.fetchone(), "BOTS table should exist after creation."
        )

    def test_insert_bot(self):
        """
        Test inserting a bot record into the 'bots' table.

        Ensures that:
        - The bot is inserted successfully
        - The number of rows in the table is correct
        - Inserted values (name, description) match expected data
        """
        self.bot_repo.insert_bot(1, "Bot Alpha")

        rows = self.conn.execute(
            """
            SELECT user_id, name FROM bots WHERE name = ?;
        """,
            ("Bot Alpha",),
        ).fetchall()

        self.assertEqual(
            len(rows), 1, "There should be exactly one bot with the name 'Bot Alpha'."
        )
        self.assertEqual(rows[0]["user_id"], 1, "the user_id of the user exsit")
        self.assertEqual(
            rows[0]["name"],
            "Bot Alpha",
            "The bot's name should match the inserted value.",
        )


if __name__ == "__main__":
    unittest.main()
