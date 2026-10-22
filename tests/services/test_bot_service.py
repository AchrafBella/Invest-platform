import os
import sys
import tempfile
import unittest

sys.path.append(os.path.join(os.getcwd(), "src"))
from database_manager import DatabaseManager
from services.bot_service import BotService


class TestBotService(unittest.TestCase):
    def setUp(self):
        self.db_file = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        self.db_file.close()
        self.database = DatabaseManager(self.db_file.name)
        self.user_id = self.database.users.insert_user("test_user")
        self.bot_service = BotService(self.db_file.name)
        return super().setUp()

    def tearDown(self):
        os.remove(self.db_file.name)
        return super().tearDown()

    def test_create_bot(self):
        response = self.bot_service.create_bot(self.user_id, "demo_bot")
        self.assertTrue(response)


if __name__ == "__main__":
    unittest.main()
