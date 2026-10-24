"""trading service"""

import logging
import os
from enum import Enum

from repositories.portfolio import PortfolioRepository
from repositories.position import PositionRepository
from repositories.transaction import TransactionRepository

DATABASE_DIR = "database"
DB_FILE = os.path.join(DATABASE_DIR, "tradingplatform.db")

logger = logging.getLogger(__name__)


class OrderSide(Enum):
    """Allowed sides for a trading order."""

    BUY = "BUY"
    SELL = "SELL"


class TradingService:
    """Coordinate order validation and repository updates."""

    def __init__(self, db_path: str = DB_FILE) -> None:
        """Initialize repositories for the selected database."""
        self.transactions = TransactionRepository(db_path)
        self.portfolios = PortfolioRepository(db_path)
        self.positions = PositionRepository(db_path)

    def _validate_order(
        self,
        user_id: int,
        portfolio_id: int,
        side: str,
        shares: int,
        ticker: str,
        price: float,
    ) -> bool:
        """Check whether the portfolio can execute the requested order."""
        if side == OrderSide.BUY.value:
            cash = self.portfolios.get_cash(user_id, portfolio_id)
            return cash >= shares * price
        if side == OrderSide.SELL.value:
            position_shares = self.positions.get_ticker(portfolio_id, ticker)
            if position_shares is None:
                return False
            return shares <= position_shares
        raise ValueError("We can only BUY & SELL.")

    def add_position(
        self,
        user_id: int,
        portfolio_id: int,
        side: str,
        ticker: str,
        shares: int,
        price: float,
    ) -> bool:
        """Validate and apply a trade to positions, cash, and transaction history."""
        if user_id is None or portfolio_id is None:
            raise ValueError(
                "There is no id assocaited with the user or the portfolio."
            )
        if shares <= 0:
            raise ValueError("Shares must be positive.")
        if price <= 0:
            raise ValueError("Price must be positive.")
        if side not in (OrderSide.BUY.value, OrderSide.SELL.value):
            raise ValueError("We can only BUY & SELL.")

        amount = shares * price

        if self._validate_order(user_id, portfolio_id, side, shares, ticker, price):
            shares_own = self.positions.get_ticker(portfolio_id, ticker)

            if side == OrderSide.BUY.value and shares_own is None:
                self.positions.insert_position(
                    portfolio_id, ticker, shares, price, amount
                )

            elif side == OrderSide.BUY.value and shares_own is not None:
                self.positions.buy_shares(portfolio_id, ticker, shares, price)

            elif OrderSide.SELL.value == side and shares_own is not None:
                self.positions.sell_shares(portfolio_id, ticker, shares, price)
                self.positions.drop_position_if_zero(portfolio_id, ticker)
            elif side == OrderSide.SELL.value:
                return False

            cash_change = amount if side == OrderSide.SELL.value else -amount
            self.portfolios.update_cash(user_id, portfolio_id, cash_change)
            self.transactions.insert_transaction(
                portfolio_id, ticker, side, price, shares
            )

            logger.info(
                "%s transaction authorized for %s amount %s.", side, ticker, amount
            )
            return True
        logger.warning(
            "Transaction rejected for portfolio %s position %s amount %s",
            portfolio_id,
            ticker,
            amount,
        )
        return False
