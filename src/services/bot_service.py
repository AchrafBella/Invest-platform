"""bot service"""

import logging
import os

from repositories.bot import BotRepository

DATABASE_DIR = "database"
DB_FILE = os.path.join(DATABASE_DIR, "tradingplatform.db")

logger = logging.getLogger(__name__)


class BotService:
    """Business operations for trading bots."""

    def __init__(self, db_file: str = DB_FILE) -> None:
        """Initialize the bot repository."""
        self.bots = BotRepository(db_file)

    def create_bot(self, user_id: int, bot_name: str) -> bool:
        """Create a bot for a user."""
        self.bots.insert_bot(user_id, bot_name)
        logger.info("Bot %s created for id = %s", bot_name, user_id)
        return True
