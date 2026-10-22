"""Transaction repository module for managing trade transaction records."""

from repositories.repository import BaseRepository


class TransactionRepository(BaseRepository):
    """Repository for managing trade transaction records in a SQLite database.

    This class tracks all buy/sell transactions with prices, quantities, and fees
    for audit and analysis purposes.
    """

    def create_table(self) -> None:
        """Create the transactions table if it does not already exist.

        The table records all trades with side type (BUY/SELL) and
        enforces positive share counts.
        """
        sql = """
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            portfolio_id INTEGER NOT NULL,
            trade_time DATETIME NOT NULL DEFAULT (CURRENT_TIMESTAMP),
            ticker TEXT NOT NULL,
            side TEXT NOT NULL,
            price REAL NOT NULL,
            shares INTEGER NOT NULL,
            fees REAL NOT NULL DEFAULT 0,
            amount REAL NOT NULL,

            CHECK (side IN ('BUY', 'SELL')),
            FOREIGN KEY (portfolio_id) REFERENCES portfolios(id)
        )
        """
        self.execute(sql)

    def insert_transaction(
        self,
        portfolio_id: int,
        ticker: str,
        side: str,
        price: float,
        shares: int,
    ) -> None:
        """Record a new transaction (buy or sell) in the database.

        Args:
            portfolio_id (int): ID of the portfolio.
            ticker (str): Stock ticker symbol.
            side (str): Either 'BUY' or 'SELL'.
            price (float): Transaction price per share.
            shares (int): Number of shares in the transaction.
        """
        sql = """
        INSERT INTO transactions (
            portfolio_id,
            trade_time,
            ticker,
            side,
            price,
            shares,
            amount
        )
        VALUES (
            :portfolio_id,
            CURRENT_TIMESTAMP,
            :ticker,
            :side,
            CASE
                WHEN :side = 'BUY' THEN -:price ELSE :price
            END,
            :shares,
            CASE
                WHEN :side = 'BUY' THEN -(:price * :shares)
                ELSE (:price * :shares)
            END
        )
    """

        params = {
            "portfolio_id": portfolio_id,
            "ticker": ticker,
            "side": side,
            "price": price,
            "shares": shares,
        }
        self.execute(sql, params)

    def list_transactions(self) -> list[dict[str, object]]:
        """Retrieve all transactions in chronological order.

        Returns:
            list[dict]: List of transaction records with portfolio_id, trade_time,
                       ticker, side, price, shares, fees, and amount.
        """
        sql = """
            SELECT
            portfolio_id,
            trade_time,
            ticker,
            side,
            price,
            shares,
            fees,
            amount
        FROM transactions
        ORDER BY trade_time, id
        """
        return self.fetch_all(sql)
