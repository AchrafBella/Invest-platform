"""
Unit tests for the BALANCE database module.
"""

import os
import sqlite3
import sys
import unittest

sys.path.append(os.path.join(os.getcwd(), "src"))

from repositories.portfolio import PortfolioRepository

DB_FILE = "src/test.db"


class TestDBBalance(unittest.TestCase):
    """Test suite for validating cash database operations."""

    def setUp(self):
        self.portfolio_repo = PortfolioRepository(DB_FILE)
        self.portfolio_repo.create_table()

        self.conn = sqlite3.connect(DB_FILE)
        self.conn.row_factory = sqlite3.Row

        return super().setUp()

    def tearDown(self):
        if self.conn:
            self.conn.close()

        if os.path.exists(DB_FILE):
            os.remove(DB_FILE)

        super().tearDown()

    def test_create_table(self):
        """Test that the cash table is created."""

        cursor = self.conn.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type='table'
            AND name='portfolios'
            """)

        self.assertIsNotNone(cursor.fetchone())

    def test_insert_portfolio(self):
        """Test inserting a new cash."""

        portfolio_id = self.portfolio_repo.insert_portfolio(
            user_id=1, name="Tech Portfolio", cash=5000
        )

        self.assertIsInstance(portfolio_id, int)

        cursor = self.conn.execute(
            """
            SELECT *
            FROM portfolios
            WHERE id = ?
            """,
            (portfolio_id,),
        )

        row = cursor.fetchone()

        self.assertIsNotNone(row)
        self.assertEqual(row["user_id"], 1)
        self.assertEqual(row["name"], "Tech Portfolio")
        self.assertEqual(row["cash"], 5000)

    def test_get_cash(self):
        """Test retrieving an existing cash."""

        portfolio_id = self.portfolio_repo.insert_portfolio(
            user_id=1, name="Tech Portfolio", cash=5000
        )

        cash = self.portfolio_repo.get_cash(user_id=1, portfolio_id=portfolio_id)

        self.assertEqual(cash, 5000)

    def test_update_cash(self):
        """Test updating an existing cash."""

        portfolio_id_1 = self.portfolio_repo.insert_portfolio(
            user_id=1, name="Tech Portfolio", cash=5000
        )

        portfolio_id_2 = self.portfolio_repo.insert_portfolio(
            user_id=1, name="Tech Portfolio", cash=7000
        )

        self.assertEqual(portfolio_id_1, portfolio_id_2)

        cash = self.portfolio_repo.get_cash(user_id=1, portfolio_id=portfolio_id_1)

        self.assertEqual(cash, 7000)

    def test_multiple_portfolios_same_user(self):
        """Test one user owning multiple portfolio cash."""

        self.portfolio_repo.insert_portfolio(
            user_id=1, name="Tech Portfolio", cash=5000
        )

        self.portfolio_repo.insert_portfolio(user_id=1, name="ETF Portfolio", cash=6000)

        cash = self.portfolio_repo.list_portfolios()

        self.assertEqual(len(cash), 2)

        names = {b["name"] for b in cash}

        self.assertIn("Tech Portfolio", names)
        self.assertIn("ETF Portfolio", names)

    def test_display_cash(self):
        """Test displaying all cash."""

        self.portfolio_repo.insert_portfolio(
            user_id=1, name="Tech Portfolio", cash=5000
        )

        self.portfolio_repo.insert_portfolio(user_id=1, name="ETF Portfolio", cash=6000)

        cash = self.portfolio_repo.list_portfolios()

        self.assertEqual(len(cash), 2)

        self.assertTrue(all("name" in item for item in cash))

        self.assertTrue(all("cash" in item for item in cash))

    def test_insert_three_portfolios_ids(self):
        """Test inserting three portfolios and checking their IDs."""

        id1 = self.portfolio_repo.insert_portfolio(
            user_id=1, name="Tech Portfolio", cash=5000
        )

        id2 = self.portfolio_repo.insert_portfolio(
            user_id=1, name="ETF Portfolio", cash=6000
        )

        id3 = self.portfolio_repo.insert_portfolio(
            user_id=2, name="Crypto Portfolio", cash=7000
        )

        self.assertNotEqual(id1, id2)
        self.assertNotEqual(id2, id3)
        self.assertNotEqual(id1, id3)

        rows = self.conn.execute("""
            SELECT id, name
            FROM portfolios
            ORDER BY id
        """).fetchall()

        self.assertEqual(len(rows), 3)

        self.assertEqual(rows[0]["id"], id1)
        self.assertEqual(rows[1]["id"], id2)
        self.assertEqual(rows[2]["id"], id3)


if __name__ == "__main__":
    unittest.main()
