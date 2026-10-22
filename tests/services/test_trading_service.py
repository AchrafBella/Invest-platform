import os
import sqlite3
import sys
import tempfile
import unittest

sys.path.append(os.path.join(os.getcwd(), "src"))
from database_manager import DatabaseManager
from services.trading_service import TradingService


class TestTradingService(unittest.TestCase):
    def setUp(self):
        self.db_file = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        self.db_file.close()
        self.database = DatabaseManager(self.db_file.name)
        self.trading_service = TradingService(self.db_file.name)
        self.user_id, self.portfolio_id = self._create_portfolio()
        self.conn = sqlite3.connect(self.db_file.name)
        self.conn.row_factory = sqlite3.Row

    def _create_portfolio(self):
        connection = sqlite3.connect(self.db_file.name)
        try:
            user_id = connection.execute(
                "INSERT INTO users (name) VALUES (?)", ("test_user",)
            ).lastrowid
            portfolio_id = connection.execute(
                "INSERT INTO portfolios (user_id, name, cash) VALUES (?, ?, ?)",
                (user_id, "test_portfolio", 5000),
            ).lastrowid
            connection.commit()
            return user_id, portfolio_id
        finally:
            connection.close()

    def tearDown(self):
        self.conn.close()
        os.remove(self.db_file.name)

    def test_buy_records_position_cash_and_transaction(self):
        result = self.trading_service.add_position(
            user_id=self.user_id,
            portfolio_id=self.portfolio_id,
            side="BUY",
            ticker="AAPL",
            shares=10,
            price=150.0,
        )

        position = self.conn.execute(
            "SELECT shares, average_price, total_invested FROM positions"
        ).fetchone()
        portfolio = self.conn.execute(
            "SELECT cash FROM portfolios WHERE id = ?", (self.portfolio_id,)
        ).fetchone()
        transaction = self.conn.execute(
            "SELECT side, ticker, shares, amount FROM transactions"
        ).fetchone()

        self.assertTrue(result)
        self.assertEqual((10, 150.0, 1500.0), tuple(position))
        self.assertEqual(3500.0, portfolio[0])
        self.assertEqual(("BUY", "AAPL", 10, -1500.0), tuple(transaction))

    def test_buy_is_rejected_when_cash_is_insufficient(self):
        result = self.trading_service.add_position(
            user_id=self.user_id,
            portfolio_id=self.portfolio_id,
            side="BUY",
            ticker="AAPL",
            shares=100,
            price=150.0,
        )

        self.assertFalse(result)
        self.assertIsNone(self.conn.execute("SELECT 1 FROM positions").fetchone())
        self.assertEqual(
            5000.0,
            self.conn.execute(
                "SELECT cash FROM portfolios WHERE id = ?", (self.portfolio_id,)
            ).fetchone()[0],
        )
        self.assertIsNone(self.conn.execute("SELECT 1 FROM transactions").fetchone())


if __name__ == "__main__":
    unittest.main()
