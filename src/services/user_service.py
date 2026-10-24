"""user service"""

import logging
import os

from repositories.user import UserRepository

DATABASE_DIR = "database"
DB_FILE = os.path.join(DATABASE_DIR, "tradingplatform.db")

logger = logging.getLogger(__name__)


class UserService:
    """Business operations for users."""

    def __init__(self, db_path: str = DB_FILE) -> None:
        """Initialize the user repository."""
        self.users = UserRepository(db_path)

    def create_user(self, user_name: str) -> int:
        """Create a user, returning the user's identifier."""
        try:
            user_id = self.users.insert_user(user_name)
            logger.info("user create with id=%s", user_id)
            return user_id
        except Exception:
            logger.exception("Error while creating the user")
            raise

    def get_user_id(self, user_name: str) -> int:
        """Look up a user's identifier by name."""
        logger.info("Resolved the user id for user %s", user_name)
        return self.users.get_user_id(user_name)
