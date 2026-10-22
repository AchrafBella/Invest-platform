"""Unit tests for the user database module."""

import os
import sqlite3
import sys
import unittest

sys.path.append(os.path.join(os.getcwd(), "src"))
from repositories.user import UserRepository

DB_FILE = "src/test.db"


class TestDBUser(unittest.TestCase):
    """
    Unit tests for database operations related to the 'users' table.
    """

    def setUp(self):
        """
        Set up an in-memory SQLite database before each test.

        - Creates a fresh database instance
        - Configures row_factory to access columns by name
        - Initializes the 'users' table
        """
        self.user_repo = UserRepository(DB_FILE)
        self.user_repo.create_table()
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
        Test the creation of the 'users' table.

        Ensures that:
        - The table is created successfully
        - The table schema matches expected structure
        """
        self.user_repo.create_table()

        # Verify that the table exists by checking the schema
        cursor = self.conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='users';"
        )
        self.assertIsNotNone(
            cursor.fetchone(), "user table should exist after creation."
        )

    def test_insert_user(self):
        """test the user insertion."""

        self.user_repo.insert_user("demo")
        row = self.conn.execute(
            """
                    SELECT * FROM users WHERE name = ?;
                """,
            ("demo",),
        ).fetchone()

        self.assertEqual(row["name"], "demo", "the user in the database")

    def test_insert_three_users(self):
        """Test inserting multiple users."""

        users = ["alice", "bob", "charlie"]

        saved_ids = {}

        for user in users:
            saved_ids[user] = self.user_repo.insert_user(user)

        rows = self.conn.execute("""
            SELECT id, name FROM users ORDER BY id;
        """).fetchall()

        self.assertEqual(len(rows), 3)

        self.assertEqual(rows[0]["name"], "alice")
        self.assertEqual(rows[1]["name"], "bob")
        self.assertEqual(rows[2]["name"], "charlie")

        self.assertEqual(saved_ids["alice"], 1)
        self.assertEqual(saved_ids["bob"], 2)
        self.assertEqual(saved_ids["charlie"], 3)


if __name__ == "__main__":
    unittest.main()
