"""Unit tests for the TRANSACTIONS database module.

This test suite verifies the correct creation and manipulation of the TRANSACTIONS table
within a SQLite database. It ensures that:
- The TRANSACTIONS table is properly created.
- Transaction records can be inserted correctly.
- Trading book data can be retrieved and displayed.
"""

import os
import sqlite3
import sys
import unittest

sys.path.append(os.path.join(os.getcwd(), "src"))
from repositories.transaction import TransactionRepository

DB_FILE = "src/test.db"


class TestDBTransaction(unittest.TestCase):
    """
    Unit tests for database operations related to the 'transactions' table.

    This test suite verifies:
    - Table creation
    - Insertion of transaction records
    - Integrity of stored data
    """

    def setUp(self):
        """
        Set up an in-memory SQLite database before each test.

        - Creates a fresh database instance
        - Configures row_factory to access columns by name
        - Initializes the 'transactions' table
        """
        self.transaction_repo = TransactionRepository(DB_FILE)
        self.transaction_repo.create_table()
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
        Test the creation of the 'transactions' table.

        Ensures that:
        - The table is created successfully
        - The table schema matches expected structure
        """
        self.transaction_repo.create_table()

        # Verify that the table exists by checking the schema
        cursor = self.conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='transactions';"
        )
        self.assertIsNotNone(
            cursor.fetchone(), "transactions table should exist after creation."
        )

    def test_insert_transaction(self):
        self.transaction_repo.insert_transaction(1, "AAPL", "BUY", 150.0, 10)
        row = self.conn.execute(
            """
                SELECT * FROM transactions WHERE portfolio_id = ?;
            """,
            (1,),
        ).fetchone()

        self.assertEqual(row["portfolio_id"], 1, "Portfolio ID should be 1.")
        self.assertEqual(row["ticker"], "AAPL", "Ticker should be 'AAPL'.")
        self.assertEqual(row["side"], "BUY", "Position should be 'BUY'.")
        self.assertEqual(row["shares"], 10, "Number of shares should be 10.")
        self.assertAlmostEqual(
            row["price"], -150.0, places=2, msg="Price should be 150.0."
        )
        self.assertAlmostEqual(
            row["amount"],
            -1500.0,
            places=2,
            msg="Amount for BUY should be negative (cost).",
        )


if __name__ == "__main__":
    unittest.main()
