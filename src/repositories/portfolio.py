"""Portfolio repository module for managing portfolio portfolio records."""

from repositories.repository import BaseRepository


class PortfolioRepository(BaseRepository):
    """Repository for managing portfolio portfolio records."""

    def create_table(self) -> None:
        """Create the portfolios table if it does not already exist."""
        sql = """
        CREATE TABLE IF NOT EXISTS portfolios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            cash REAL NOT NULL DEFAULT 0.0,

            CHECK (cash >= 0),
            UNIQUE (user_id, name),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
        """
        self.execute(sql)

    def insert_portfolio(self, user_id: int, name: str, cash: float) -> int:
        """
        Create or update a portfolio portfolio.

        Returns:
            int: portfolio_id
        """

        sql = """
        INSERT INTO portfolios (
            user_id,
            name,
            date,
            cash
        )
        VALUES (
            :user_id,
            :name,
            CURRENT_TIMESTAMP,
            :cash
        )
        ON CONFLICT(user_id, name)
        DO UPDATE SET
            cash = EXCLUDED.cash,
            date = CURRENT_TIMESTAMP
        """

        params = {"user_id": user_id, "name": name, "cash": cash}
        self.execute(sql, params)
        sql = """
                        SELECT id
                        FROM portfolios
                        WHERE user_id = :user_id
                        AND name = :name
                        """
        params = {"user_id": user_id, "name": name}
        row = self.fetch_one(sql, params)
        portfolio_id = row.get("id")
        if portfolio_id is None:
            raise ValueError(
                f"Portfolio not found for user_id={user_id} and name={name}"
            )
        return int(portfolio_id)

    def update_cash(self, user_id: int, portfolio_id: int, cash_change: float) -> None:
        """
        Update the cash balance of a portfolio.

        Args:
            user_id (int): ID of the user.
            portfolio_id (int): ID of the portfolio.
            cash_change (float): Amount to change the cash balance by (can be positive or negative).
        """
        sql = """
        UPDATE portfolios
        SET cash = cash + :cash_change
        WHERE user_id = :user_id
        AND id = :portfolio_id
        """
        params = {
            "user_id": user_id,
            "portfolio_id": portfolio_id,
            "cash_change": cash_change,
        }
        self.execute(sql, params)

    def get_cash(self, user_id: int, portfolio_id: int) -> float:
        """
        Retrieve a cash from portfolio.
        """
        sql = """
        SELECT cash
        FROM portfolios
        WHERE user_id = :user_id
        AND id = :portfolio_id
        """

        params = {"user_id": user_id, "portfolio_id": portfolio_id}
        row = self.fetch_one(sql, params)
        cash = row.get("cash")
        if cash is None:
            return 0.0
        return float(cash)

    def get_portfolio_id(self, user_id: int, portfolio_name: str) -> int:
        """Look up a portfolio identifier by user and portfolio name."""
        sql = """
        SELECT id, user_id, name FROM portfolios WHERE user_id = :user_id AND name = :name LIMIT 1
        """
        params = {"name": portfolio_name, "user_id": user_id}
        row = self.fetch_one(sql, params)
        portfolio_id = row.get("id")
        if portfolio_id is None:
            raise ValueError(
                f"Portfolio not found for user_id={user_id} and name={portfolio_name}"
            )
        return int(portfolio_id)

    def list_portfolios(self) -> list:
        """
        Retrieve all portfolios.
        """

        sql = """
        SELECT
            id,
            user_id,
            name,
            cash,
            date
        FROM portfolios
        ORDER BY user_id, name
        """
        return self.fetch_all(sql)

    def delete_portfolio(self, user_id: int, name: str) -> None:
        """Delete a portfolio belonging to a user."""

        sql = """
        DELETE FROM portfolios
        WHERE user_id = :user_id
        AND name = :name
        """
        params = {"user_id": user_id, "name": name}
        self.execute(sql, params)
