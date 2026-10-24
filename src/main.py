"""Seed the trading database with example portfolios when run directly."""

# from bots.simple_bot import TradingBot
from database_manager import DatabaseManager
from services.portfolio_service import PortfolioService
from services.trading_service import TradingService
from services.user_service import UserService

if __name__ == "__main__":
    DatabaseManager()

    trading_service = TradingService()
    portfolio_service = PortfolioService()
    user_service = UserService()

    positions2 = [
        {
            "user_name": "achraf",
            "name": "Tech Portfolio",
            "balance": 15_000,
            "values": [
                {"ticker": "AAPL", "shares": 40, "average_price": 200},
                {"ticker": "MSFT", "shares": 1, "average_price": 420},
                {"ticker": "GOOG", "shares": 2, "average_price": 240},
            ],
        },
    ]

    positions = [
        {
            "user_name": "achraf",
            "name": "Tech Portfolio",
            "balance": 15_000,
            "values": [
                {"ticker": "AAPL", "shares": 15, "average_price": 175},
                {"ticker": "MSFT", "shares": 8, "average_price": 320},
                {"ticker": "GOOG", "shares": 5, "average_price": 140},
            ],
        },
        {
            "user_name": "achraf",
            "name": "Crypto Portfolio",
            "balance": 7_000,
            "values": [
                {"ticker": "BTC", "shares": 1, "average_price": 45_000},
                {"ticker": "ETH", "shares": 5, "average_price": 2_500},
            ],
        },
        {
            "user_name": "karima",
            "name": "Growth Portfolio",
            "balance": 12_000,
            "values": [
                {"ticker": "NVDA", "shares": 10, "average_price": 900},
                {"ticker": "TSLA", "shares": 12, "average_price": 220},
            ],
        },
        {
            "user_name": "karima",
            "name": "Dividend Portfolio",
            "balance": 9_000,
            "values": [
                {"ticker": "KO", "shares": 50, "average_price": 60},
                {"ticker": "PEP", "shares": 25, "average_price": 180},
                {"ticker": "JNJ", "shares": 20, "average_price": 155},
            ],
        },
        {
            "user_name": "youssef",
            "name": "Tech Portfolio",
            "balance": 20_000,
            "values": [
                {"ticker": "AAPL", "shares": 30, "average_price": 170},
                {"ticker": "AMZN", "shares": 20, "average_price": 135},
                {"ticker": "META", "shares": 10, "average_price": 450},
            ],
        },
        {
            "user_name": "sara",
            "name": "Crypto Portfolio",
            "balance": 10_000,
            "values": [
                {"ticker": "BTC", "shares": 2, "average_price": 43_000},
                {"ticker": "SOL", "shares": 50, "average_price": 110},
                {"ticker": "ADA", "shares": 500, "average_price": 0.55},
            ],
        },
        {
            "user_name": "hamza",
            "name": "ETF Portfolio",
            "balance": 18_000,
            "values": [
                {"ticker": "SPY", "shares": 20, "average_price": 500},
                {"ticker": "QQQ", "shares": 15, "average_price": 430},
            ],
        },
        {
            "user_name": "fatima",
            "name": "Long Term Portfolio",
            "balance": 25_000,
            "values": [
                {"ticker": "BRK.B", "shares": 12, "average_price": 410},
                {"ticker": "V", "shares": 25, "average_price": 270},
                {"ticker": "MA", "shares": 15, "average_price": 460},
            ],
        },
        {
            "user_name": "omar",
            "name": "AI Portfolio",
            "balance": 16_000,
            "values": [
                {"ticker": "NVDA", "shares": 8, "average_price": 950},
                {"ticker": "AMD", "shares": 20, "average_price": 170},
                {"ticker": "PLTR", "shares": 50, "average_price": 25},
            ],
        },
        {
            "user_name": "layla",
            "name": "Mixed Portfolio",
            "balance": 14_000,
            "values": [
                {"ticker": "AAPL", "shares": 10, "average_price": 180},
                {"ticker": "BTC", "shares": 1, "average_price": 47_000},
                {"ticker": "SPY", "shares": 8, "average_price": 510},
            ],
        },
    ]

    # for port in positions:
    #     values = port.get("values")
    #     if not isinstance(values, list):
    #         continue

    #     user_name = port.get("user_name")
    #     portfolio_name = port.get("name")
    #     balance = port.get("balance")
    #     if not isinstance(user_name, str) or not isinstance(portfolio_name, str):
    #         continue
    #     if not isinstance(balance, (int, float)):
    #         continue

    #     user_id, portfolio_id = user_service.crea(
    #         user_name,
    #         portfolio_name,
    #         float(balance),
    #     )
    #     for elm in values:
    #         if not isinstance(elm, dict):
    #             continue
    #         ticker = elm.get("ticker")
    #         shares = elm.get("shares")
    #         average_price = elm.get("average_price")
    #         if not isinstance(ticker, str) or not isinstance(shares, int):
    #             continue
    #         if not isinstance(average_price, (int, float)):
    #             continue
    #         trading_service.add_position(
    #             user_id,
    #             portfolio_id,
    #             "BUY",
    #             ticker,
    #             shares,
    #             float(average_price),
    #         )

    for port in positions2:
        values = port.get("values")
        if not isinstance(values, list):
            continue

        user_name = port.get("user_name")
        portfolio_name = port.get("name")
        balance = port.get("balance")
        if (
            not isinstance(user_name, str)
            or not isinstance(portfolio_name, str)
            or not isinstance(balance, (int, float))
        ):
            continue

        user_id = user_service.create_user(user_name)
        portfolio_id = portfolio_service.create_portfolio(
            user_id, portfolio_name, float(balance)
        )
        for elm in values:
            if not isinstance(elm, dict):
                continue
            ticker = elm.get("ticker")
            shares = elm.get("shares")
            average_price = elm.get("average_price")
            if not isinstance(ticker, str) or not isinstance(shares, int):
                continue
            if not isinstance(average_price, (int, float)):
                continue
            trading_service.add_position(
                user_id,
                portfolio_id,
                "BUY",
                ticker,
                shares,
                float(average_price),
            )

    # user_id = user_service.get_user_id("achraf")
    # portfolio_id = user_service.get_portfolio_id(user_id, "Tech Portfolio")
    # trading_service.add_position(user_id, portfolio_id, "SELL", "AAPL", 50, 190)

    # user_id = user_service.get_user_id("achraf")
    # portfolio_id = user_service.get_portfolio_id(user_id, "Tech Portfolio")
    # trading_service.add_position(user_id, portfolio_id, "SELL", "AAPL", 4, 190)

    # user_id = user_service.get_user_id("omar")
    # portfolio_id = user_service.get_portfolio_id(user_id, "AI Portfolio")
    # trading_service.add_position(user_id, portfolio_id, "SELL", "NVDA", 3, 1200)

    # portfolio_id = UserService.get_portfolio_id_by_name(2, "demo_2")
    # print(portfolio_id)

    # user_id = UserService.get_user_id_by_name("achraf_2")
    # print(user_id)

    # tickers = [
    #     "AAPL",
    #     "MSFT",
    #     "GOOGL",
    #     "AMZN",
    #     "META",
    #     "TSLA",
    #     "NVDA",
    #     "NFLX",
    #     "JPM",
    #     "V",
    #     "MC.PA",
    #     "AIR.PA",
    #     "OR.PA",
    #     "SAN.PA",
    #     "BNP.PA",
    #     "SAP.DE",
    #     "SIE.DE",
    #     "BMW.DE",
    #     "ALV.DE",
    #     "VOD.L",
    #     "HSBA.L",
    #     "SHEL.L",
    #     "ASML.AS",
    #     "NESN.SW",
    #     "NOVN.SW",
    # ]

    # bot = TradingBot("demo", tickers, 5)
    # signal_list = bot.signal()
    # print(signal_list)
