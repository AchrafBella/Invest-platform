import os
import sys
import tempfile
import unittest

sys.path.append(os.path.join(os.getcwd(), "src"))
from database_manager import DatabaseManager
from services.portfolio_service import PortfolioService
from services.user_service import UserService


class TestUserService(unittest.TestCase):
    def setUp(self):
        self.db_file = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        self.db_file.close()
        self.database = DatabaseManager(self.db_file.name)
        self.user_service = UserService(self.db_file.name)
        return super().setUp()

    def tearDown(self):
        os.remove(self.db_file.name)
        return super().tearDown()

    def test_create_user(self):
        response_id = self.user_service.create_user("demo_user")
        self.assertIsNotNone(response_id)
        self.assertIsInstance(response_id, int)

    def test_user_and_portfolio_services_are_separate(self):
        user_id = self.user_service.create_user("demo_user")
        portfolio_service = PortfolioService(self.db_file.name)

        portfolio_id = portfolio_service.create_portfolio(
            user_id, "demo_portfolio", 5000
        )

        self.assertEqual(
            portfolio_id,
            portfolio_service.get_portfolio_id(user_id, "demo_portfolio"),
        )


if __name__ == "__main__":
    unittest.main()
