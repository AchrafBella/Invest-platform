"""Portfolio repository module for managing investment portfolio holdings."""

from repositories.repository import BaseRepository


class PositionRepository(BaseRepository):
    """Repository for managing investment Position holdings in a SQLite database.

    This class provides CRUD operations for Position management, including
    buying/selling shares, tracking performance, and calculating gains.
    """

    def create_table(self) -> None:
        """Create the Positions table if it does not already exist.

        The table tracks individual holdings with performance metrics and gains.
        Enforces positive share counts and average prices with unique constraint
        on (name, ticker) pair.
        """
        sql = """
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            portfolio_id INTEGER NOT NULL,
            ticker TEXT NOT NULL,
            shares INTEGER NOT NULL,
            average_price REAL NOT NULL,
            total_invested REAL NOT NULL DEFAULT 0,
            performance REAL NOT NULL DEFAULT 0,
            gain_unrealized REAL NOT NULL DEFAULT 0,
            gain_realized REAL NOT NULL DEFAULT 0,
            creation_date DATETIME NOT NULL DEFAULT (CURRENT_TIMESTAMP),

            CHECK (average_price >= 0),
            UNIQUE (portfolio_id, ticker),
            FOREIGN KEY (portfolio_id) REFERENCES portfolios(id)
        )
        """
        self.execute(sql)

    def insert_position(
        self,
        portfolio_id: int,
        ticker: str,
        shares: int,
        average_price: float,
        total_invested: float,
    ) -> int:
        """Insert a new Position holding into the database.

        Args:
            user_id (int): ID of the Position owner.
            ticker (str): Stock ticker symbol.
            shares (int): Number of shares.
            average_price (float): Average purchase price per share.
            total_invested (float): Total amount invested.
        """
        sql = """
        INSERT INTO positions (
            portfolio_id,
            ticker,
            shares,
            average_price,
            total_invested
        )
        VALUES (
            :portfolio_id,
            :ticker,
            :shares,
            :average_price,
            :total_invested
        )
        """
        params = {
            "portfolio_id": portfolio_id,
            "ticker": ticker,
            "shares": shares,
            "average_price": average_price,
            "total_invested": total_invested,
        }
        return self.execute(sql, params)

    def buy_shares(
        self, portfolio_id: int, ticker: str, shares: int, price: float
    ) -> None:
        """Update Position when buying shares.

        Recalculates average price, total invested amount, and performance metrics.

        Args:
            portfolio_id (int): ID of the Position owner.
            ticker (str): Stock ticker symbol.
            shares (int): Number of shares to buy.
            price (float): Purchase price per share.
        """
        sql = """
                UPDATE positions
                    SET
                        shares = shares + :shares,
                        total_invested = total_invested + (:price * :shares),
                        average_price =
                            ((average_price * shares) + (:price * :shares))
                            / (shares + :shares),
                        gain_unrealized =
                            (:price * (shares + :shares))
                            - (total_invested + (:price * :shares)),
                        performance =
                            (
                                (:price * (shares + :shares))
                                - (total_invested + (:price * :shares))
                            ) * 100.0
                            / (total_invested + (:price * :shares))
                    WHERE ticker = :ticker
                    AND portfolio_id = :portfolio_id;
        """
        params = {
            "portfolio_id": portfolio_id,
            "ticker": ticker,
            "shares": shares,
            "price": price,
        }
        self.execute(sql, params)

    def sell_shares(
        self, portfolio_id: int, ticker: str, shares: int, price: float
    ) -> None:
        """Update Position when selling shares.

        Recalculates realized gains, unrealized gains, and performance metrics.

        Args:
            portfolio_id (int): ID of the Position owner.
            ticker (str): Stock ticker symbol.
            shares (int): Number of shares to sell.
            price (float): Sale price per share.
        """
        sql = """
                UPDATE positions
                    SET
                        shares = shares - :shares,
                        total_invested = total_invested - (average_price * :shares),
                        gain_realized =
                            gain_realized + (:price * :shares)
                            - (average_price * :shares),
                        gain_unrealized =
                            (:price * (shares - :shares))
                            - (total_invested - (average_price * :shares)),
                        performance =
                            CASE
                                WHEN (total_invested - (average_price * :shares)) > 0
                                THEN ((:price * (shares - :shares)) - (total_invested - (average_price * :shares))) * 100.0 / (total_invested - (average_price * :shares))
                                ELSE 0
                            END
                    WHERE ticker = :ticker
                    AND portfolio_id = :portfolio_id;
        """
        params = {
            "portfolio_id": portfolio_id,
            "ticker": ticker,
            "shares": shares,
            "price": price,
        }
        self.execute(sql, params)

    def get_ticker(self, portfolio_id: int, ticker: str) -> int | None:
        """Return the share count for a ticker in a portfolio."""
        sql = """
        SELECT shares FROM positions WHERE portfolio_id = :portfolio_id AND ticker = :ticker
        """
        params = {"portfolio_id": portfolio_id, "ticker": ticker}
        row = self.fetch_one(sql, params)
        shares = row.get("shares")
        if shares is None:
            return None
        return int(shares)

    def update_performance(
        self, portfolio_id: int, ticker: str, current_price: float
    ) -> None:
        """Update unrealized gains and performance metrics with current market price.

        Args:
            portfolio_id (int): ID of the Position owner.
            ticker (str): Stock ticker symbol.
            current_price (float): Current market price per share.
        """
        sql = """
                UPDATE positions
                    SET
                        gain_unrealized =
                            (:current_price * shares)
                            - total_invested,
                        performance =
                            CASE
                                WHEN total_invested > 0
                                THEN (
                                    (:current_price * shares)
                                    - total_invested
                                ) * 100.0
                                / total_invested
                                ELSE 0
                            END
                    WHERE ticker = :ticker
                    AND portfolio_id = :portfolio_id;
        """
        params = {
            "portfolio_id": portfolio_id,
            "ticker": ticker,
            "current_price": current_price,
        }
        self.execute(sql, params)

    def drop_position_if_zero(self, portfolio_id: int, ticker: str) -> None:
        """Delete a Position position from the database.

        Args:
            portfolio_id (int): ID of the Position owner.
            ticker (str): Stock ticker symbol.
        """
        sql = """
        DELETE FROM positions
        WHERE portfolio_id = :portfolio_id AND ticker = :ticker AND shares = 0
        """
        params = {"portfolio_id": portfolio_id, "ticker": ticker}
        self.execute(sql, params)

    def list_positions(self) -> list[dict]:
        """Retrieve all Position positions from the database.

        Returns:
            list[dict]: List of Position records with all position details.
        """
        sql = """
        SELECT id, portfolio_id, ticker, shares, average_price, total_invested, performance, gain_unrealized, gain_realized, creation_date
        FROM positions
        """
        return self.fetch_all(sql)
