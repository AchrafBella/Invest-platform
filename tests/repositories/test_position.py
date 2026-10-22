import os
import sqlite3
import sys
import unittest

sys.path.append(os.path.join(os.getcwd(), "src"))
from repositories.position import PositionRepository

DB_FILE = "src/test.db"


class TestDBPosition(unittest.TestCase):
    """
    Unit tests for database operations related to the 'positions' table.

    This test suite verifies:
    - Table creation
    - Insertion of portfolio records
    - Integrity of stored data
    """

    def setUp(self):
        """
        Set up an in-memory SQLite database before each test.

        - Creates a fresh database instance
        - Configures row_factory to access columns by name
        - Initializes the 'positions' table
        """
        self.position_repo = PositionRepository(DB_FILE)
        self.position_repo.create_table()
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
        Test the creation of the 'positions' table.

        Ensures that:
        - The table is created successfully
        - The table schema matches expected structure
        """
        self.position_repo.create_table()

        # Verify that the table exists by checking the schema
        cursor = self.conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='positions';"
        )
        self.assertIsNotNone(
            cursor.fetchone(), "positions table should exist after creation."
        )

    def test_insert_position(self):
        """
        Test inserting a portfolio record into the 'positions' table.

        Ensures that:
        - The portfolio is inserted successfully
        - The number of rows in the table is correct
        - Inserted values (name, ticker, shares, average_price, total_invested) match expected data
        """
        self.position_repo.insert_position(1, "AAPL", 10, 150.0, 1500.0)

        rows = self.conn.execute(
            """
            SELECT ticker, shares, average_price, total_invested FROM positions WHERE portfolio_id = ?;
        """,
            (1,),
        ).fetchall()

        self.assertEqual(
            len(rows),
            1,
            "There should be exactly one portfolio with the name 'Portfolio1'.",
        )
        self.assertEqual(
            rows[0]["ticker"],
            "AAPL",
            "The portfolio's ticker should match the inserted value.",
        )
        self.assertEqual(
            rows[0]["shares"],
            10,
            "The portfolio's shares should match the inserted value.",
        )
        self.assertEqual(
            rows[0]["average_price"],
            150.0,
            "The portfolio's average price should match the inserted value.",
        )
        self.assertEqual(
            rows[0]["total_invested"],
            1500.0,
            "The portfolio's total invested should match the inserted value.",
        )

    def test_insert_multiple_positions(self):
        """
        Test inserting multiple portfolio records into the 'positions' table.

        Ensures that:
        - Multiple positions can be inserted successfully
        - The number of rows in the table is correct
        - Inserted values for each portfolio match expected data
        """
        positions = [
            (1, "AAPL", 10, 150.0, 1500.0),
            (1, "GOOGL", 5, 2000.0, 10000.0),
            (1, "MSFT", 20, 250.0, 5000.0),
        ]

        for portfolio_id, ticker, shares, avg_price, total_invested in positions:
            self.position_repo.insert_position(
                portfolio_id, ticker, shares, avg_price, total_invested
            )

        rows = self.conn.execute(
            "SELECT portfolio_id, ticker, shares, average_price, total_invested FROM positions;"
        ).fetchall()
        self.assertEqual(
            len(rows),
            len(positions),
            f"There should be exactly {len(positions)} positions in the table.",
        )

        for i, (portfolio_id, ticker, shares, avg_price, total_invested) in enumerate(
            positions
        ):
            self.assertEqual(rows[i]["portfolio_id"], portfolio_id)
            self.assertEqual(rows[i]["ticker"], ticker)
            self.assertEqual(rows[i]["shares"], shares)
            self.assertEqual(rows[i]["average_price"], avg_price)
            self.assertEqual(rows[i]["total_invested"], total_invested)

    def test_buy_shares_updates_portfolio(self):
        """
        Test that buying shares updates the portfolio correctly.

        Ensures that:
        - The number of shares increases
        - The average price is recalculated correctly
        - The total invested amount is updated correctly
        """
        self.position_repo.insert_position(1, "AAPL", 10, 150.0, 1500.0)

        self.position_repo.buy_shares(1, "AAPL", 5, 160.0)  # Buying 5 more at $160

        row = self.conn.execute(
            """
            SELECT ticker, shares, average_price, total_invested FROM positions WHERE portfolio_id = ?;
        """,
            (1,),
        ).fetchone()

        expected_shares = 15  # 10 + 5
        expected_average_price = (10 * 150.0 + 5 * 160.0) / expected_shares
        expected_total_invested = expected_shares * expected_average_price

        self.assertEqual(
            row["shares"],
            expected_shares,
            "The number of shares should be updated correctly.",
        )
        self.assertAlmostEqual(
            row["average_price"],
            expected_average_price,
            places=2,
            msg="The average price should be recalculated correctly.",
        )
        self.assertAlmostEqual(
            row["total_invested"],
            expected_total_invested,
            places=2,
            msg="The total invested amount should be updated correctly.",
        )

    def test_sell_shares_updates_portfolio(self):
        """
        Test that selling shares updates the portfolio correctly.

        Ensures that:
        - The number of shares decreases
        - The average price remains unchanged
        - The total invested amount is updated correctly
        """
        self.position_repo.insert_position(1, "AAPL", 10, 150.0, 1500.0)

        self.position_repo.sell_shares(1, "AAPL", 5, 100.0)  # Selling 5 shares at $100

        row = self.conn.execute(
            """
            SELECT ticker, shares, average_price, total_invested FROM positions WHERE portfolio_id = ?;
        """,
            (1,),
        ).fetchone()

        expected_shares = 5  # 10 - 5
        expected_average_price = 150.0  # Average price remains the same after selling
        expected_total_invested = expected_shares * expected_average_price

        self.assertEqual(
            row["shares"],
            expected_shares,
            "The number of shares should be updated correctly after selling.",
        )
        self.assertAlmostEqual(
            row["average_price"],
            expected_average_price,
            places=2,
            msg="The average price should remain unchanged after selling.",
        )
        self.assertAlmostEqual(
            row["total_invested"],
            expected_total_invested,
            places=2,
            msg="The total invested amount should be updated correctly after selling.",
        )

    def test_get_shares(self):
        self.position_repo.insert_position(1, "AAPL", 10, 150.0, 1500.0)
        self.position_repo.insert_position(1, "GOOG", 50, 150.0, 1500.0)
        self.position_repo.insert_position(1, "MSFT", 60, 150.0, 1500.0)

        aapl_shares = self.position_repo.get_ticker(1, "AAPL")
        goog_shares = self.position_repo.get_ticker(1, "GOOG")
        msft_shares = self.position_repo.get_ticker(1, "MSFT")

        self.assertEqual(10, aapl_shares)
        self.assertEqual(50, goog_shares)
        self.assertEqual(60, msft_shares)


if __name__ == "__main__":
    unittest.main()
