"""Business operations for portfolios."""

import logging
import os

from repositories.portfolio import PortfolioRepository

DATABASE_DIR = "database"
DB_FILE = os.path.join(DATABASE_DIR, "tradingplatform.db")

logger = logging.getLogger(__name__)


class PortfolioService:
    """Create portfolios and look up their identifiers."""

    def __init__(self, db_path: str = DB_FILE) -> None:
        """Initialize the portfolio repository."""
        self.portfolios = PortfolioRepository(db_path)

    def create_portfolio(self, user_id: int, portfolio_name: str, cash: float) -> int:
        """Create a portfolio and return its identifier."""
        try:
            portfolio_id = self.portfolios.insert_portfolio(
                user_id, portfolio_name, cash
            )
            logger.info(
                "Cash initialized for user id=%s's portfolio cash: %s", user_id, cash
            )
            return portfolio_id
        except Exception:
            logger.exception("Error while creating the portfolio")
            raise

    def get_portfolio_id(self, user_id: int, portfolio_name: str) -> int:
        """Look up a portfolio identifier by user and portfolio name."""
        logger.info(
            "Resolved the portfolio id for user %s and portfolio %s",
            user_id,
            portfolio_name,
        )
        return self.portfolios.get_portfolio_id(user_id, portfolio_name)
