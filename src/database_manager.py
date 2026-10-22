"""
Central manager for all repositories.
Responsible for initializing repositories, creating database tables,
and coordinating operations between users, position, transactions,
portfolios, and bots.
"""

import logging
import os
from pathlib import Path

from repositories.bot import BotRepository
from repositories.portfolio import PortfolioRepository
from repositories.position import PositionRepository
from repositories.transaction import TransactionRepository
from repositories.user import UserRepository

LOG_FILE = "logs/tradingplatform.log"
DATABASE_DIR = "database"
DB_FILE = os.path.join(DATABASE_DIR, "tradingplatform.db")

logger = logging.getLogger()
Path(LOG_FILE).parent.mkdir(parents=True, exist_ok=True)
file_handler = logging.FileHandler(LOG_FILE)
file_handler.setFormatter(
    logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s")
)

logger.addHandler(file_handler)
logger.setLevel(getattr(logging, "INFO", logging.INFO))


class DatabaseManager:
    """Initialize database repositories and create their tables."""

    def __init__(self, db_path: str = DB_FILE) -> None:
        os.makedirs(DATABASE_DIR, exist_ok=True)

        self.transactions = TransactionRepository(db_path)
        self.portfolios = PortfolioRepository(db_path)
        self.positions = PositionRepository(db_path)
        self.users = UserRepository(db_path)
        self.bots = BotRepository(db_path)
        self._init_tables()
        logger.info("DatabaseManager initialized with repositories.")

    def _init_tables(self) -> None:
        for repo in (
            self.users,
            self.transactions,
            self.positions,
            self.portfolios,
            self.bots,
        ):
            repo.create_table()
        logger.info("Tables created.")
