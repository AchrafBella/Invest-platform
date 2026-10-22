"""Helpers for downloading market data used by the trading bots."""

import logging

import pandas as pd
import yfinance as yf

logger = logging.getLogger(__name__)

VALID_INTERVALS = {
    "1m",
    "2m",
    "5m",
    "15m",
    "30m",
    "60m",
    "90m",
    "1h",
    "4h",
    "1d",
    "5d",
    "1wk",
    "1mo",
    "3mo",
}


def fetch_data(
    tickers: str | list[str],
    interval: str,
    period: str,
    auto_adjust: bool = True,
    prepost: bool = False,
) -> pd.DataFrame:
    """
    Download historical market data from Yahoo Finance.

    Fetches OHLCV data for one or multiple tickers using the yfinance API.
    Validates the requested interval and ensures data is returned.

    Args:
        tickers (list[str]): List of ticker symbols to fetch data for.
        interval (str): Data interval (must be in VALID_INTERVALS).
        period (str): Data period (e.g. "1d", "1mo", "1y").
        auto_adjust (bool): Adjust prices for splits/dividends. Default is True.
        prepost (bool): Include pre/post market data. Default is False.

    Returns:
        pd.DataFrame: DataFrame containing historical market data.

    Raises:
        ValueError: If interval is invalid or no data is returned.
        RuntimeError: If Yahoo Finance download fails.
    """

    if interval not in VALID_INTERVALS:
        raise ValueError(
            f"Invalid interval {interval}. Allowed: {sorted(VALID_INTERVALS)}"
        )

    if isinstance(tickers, list):
        tickers = " ".join(tickers)

    try:
        df = yf.download(
            tickers,
            interval=interval,
            period=period,
            auto_adjust=auto_adjust,
            prepost=prepost,
            progress=False,
            threads=True,
        )
    except Exception as exc:
        logger.exception("Download failed")
        raise RuntimeError("Download failed") from exc

    if df is None or df.empty:
        logger.error(
            "No data returned. Possible reasons: invalid ticker, too short period, or Yahoo throttling."
        )
        raise ValueError(
            "No data returned. Possible reasons: invalid ticker, too short period, or Yahoo throttling."
        )

    return df
