import os
import sys
import unittest
from unittest.mock import patch

import pandas as pd

sys.path.append(os.path.join(os.getcwd(), "src"))
from bots.simple_bot import BUY_SIGNAL, SELL_SIGNAL, TradingBot


class TestTradingBot(unittest.TestCase):
    """
    Unit tests for the TradingBot class.

    This test suite verifies:
    - Bot initialization with various parameters
    - Signal generation for BUY/SELL conditions
    - Threshold functionality
    - Error handling during data fetching
    """

    def setUp(self):
        """Set up test fixtures before each test."""
        self.bot_name = "TestBot"
        self.stocks_watch_list = ["AAPL", "GOOGL", "MSFT"]
        self.default_threshold_buy = -0.30
        self.default_threshold_sell = 0.30

    def test_bot_initialization_with_defaults(self):
        """Test TradingBot initialization with default parameters."""
        bot = TradingBot(
            bot_name=self.bot_name, stocks_watch_list=self.stocks_watch_list
        )

        self.assertEqual(bot.bot_name, self.bot_name)
        self.assertEqual(bot.stocks_watch_list, self.stocks_watch_list)
        self.assertEqual(bot.threshold_buy, self.default_threshold_buy)
        self.assertEqual(bot.threshold_sell, self.default_threshold_sell)
        self.assertEqual(bot.pct_change_period, 5)

    def test_bot_initialization_with_custom_thresholds(self):
        """Test TradingBot initialization with custom threshold parameters."""
        custom_buy = -0.50
        custom_sell = 0.50
        custom_period = 10

        bot = TradingBot(
            bot_name=self.bot_name,
            stocks_watch_list=self.stocks_watch_list,
            threshold_buy=custom_buy,
            threshold_sell=custom_sell,
            pct_change_period=custom_period,
        )

        self.assertEqual(bot.threshold_buy, custom_buy)
        self.assertEqual(bot.threshold_sell, custom_sell)
        self.assertEqual(bot.pct_change_period, custom_period)

    @patch("bots.simple_bot.fetch_data")
    def test_signal_generation_buy_condition(self, mock_fetch_data):
        # Create daily data with 6+ points for 5-period pct_change computation
        # Price drops from 150 to 105 = -30% (meets threshold_buy of -0.30/-30%)
        df_daily = pd.DataFrame({("Close", "AAPL"): [150, 145, 140, 135, 130, 105]})

        # Mock intraday data
        df_intraday = pd.DataFrame({("Close", "AAPL"): [104]})

        mock_fetch_data.side_effect = [df_daily, df_intraday]

        bot = TradingBot(
            bot_name=self.bot_name,
            stocks_watch_list=["AAPL"],
            threshold_buy=-0.30,
            threshold_sell=0.30,
            pct_change_period=5,
        )

        signals = bot.signal()
        self.assertEqual(len(signals), 1)
        self.assertEqual(signals[0].signal, BUY_SIGNAL)
        self.assertAlmostEqual(signals[0].pct_change, -30.0)

    def test_signal_generation_sell_condition(self):
        # Create daily data with 6+ points for 5-period pct_change computation
        # Price rises from 100 to 130 = +30% (meets threshold_sell of 0.30/+30%)
        df_daily = pd.DataFrame({("Close", "GOOGL"): [100, 105, 110, 115, 120, 130]})

        # Mock intraday data
        df_intraday = pd.DataFrame({("Close", "GOOGL"): [131]})

        with patch("bots.simple_bot.fetch_data", side_effect=[df_daily, df_intraday]):
            bot = TradingBot(
                bot_name=self.bot_name,
                stocks_watch_list=["GOOGL"],
                threshold_buy=-0.30,
                threshold_sell=0.30,
                pct_change_period=5,
            )

            signals = bot.signal()
            self.assertEqual(len(signals), 1)
            self.assertEqual(signals[0].signal, SELL_SIGNAL)
            self.assertAlmostEqual(signals[0].pct_change, 30.0)

    @patch("bots.simple_bot.fetch_data")
    def test_signal_respects_custom_thresholds(self, mock_fetch_data):
        df_daily = pd.DataFrame({("Close", "AAPL"): [100, 99, 98, 97, 96, 95]})
        mock_fetch_data.return_value = df_daily

        bot = TradingBot(
            bot_name=self.bot_name,
            stocks_watch_list=["AAPL"],
            threshold_buy=-0.10,
            threshold_sell=0.10,
            pct_change_period=5,
        )

        self.assertEqual(bot.signal(), [])
        mock_fetch_data.assert_called_once_with("AAPL", interval="1d", period="10d")


if __name__ == "__main__":
    unittest.main()
