"""Pydantic request and response models for the API."""

from typing import Literal

from pydantic import BaseModel, Field


class UserIdResponse(BaseModel):
    """API response containing a user identifier."""

    error: bool = Field(..., description="Indicates if there was an error")
    message: str = Field(..., description="Message describing the result")
    user_id: int = Field(..., description="ID of the user")


class PortfolioIdResponse(BaseModel):
    """API response containing a portfolio identifier."""

    error: bool = Field(..., description="Indicates if there was an error")
    message: str = Field(..., description="Message describing the result")
    portfolio_id: int = Field(..., description="ID of the portfolio")


class CreateUserPortfolioResponse(BaseModel):
    """API response after creating a user and portfolio."""

    error: bool = Field(..., description="Indicates if there was an error")
    message: str = Field(..., description="Message describing the result")
    user_id: int = Field(..., description="ID of the user")
    portfolio_id: int = Field(..., description="ID of the portfolio")


class CreateUserPortfolioInput(BaseModel):
    """Request to create a user and initial portfolio."""

    name: str = Field(..., min_length=1, description="User name")
    portfolio_name: str = Field(..., min_length=1, description="Portfolio name")
    balance: float = Field(..., ge=0, description="Initial portfolio balance")


class AddPortfolioResponse(BaseModel):
    """API response after adding a portfolio."""

    error: bool = Field(..., description="Indicates if there was an error")
    message: str = Field(..., description="Message describing the result")
    portfolio_id: int = Field(..., description="ID of the portfolio")


class AddPortfolioInput(BaseModel):
    """Request to add a portfolio to an existing user."""

    user_id: int = Field(..., description="ID of the user")
    portfolio_name: str = Field(..., min_length=1, description="Portfolio name")
    balance: float = Field(..., ge=0, description="Initial portfolio balance")


class MarketOrderInput(BaseModel):
    """Validated market-order request."""

    user_id: int = Field(..., description="ID of the user")
    portfolio_id: int = Field(..., description="ID of the portfolio")
    side: Literal["BUY", "SELL"] = Field(
        ..., description="Side of the order (BUY or SELL)"
    )
    ticker: str = Field(..., description="Ticker symbol of the asset")
    shares: int = Field(gt=0, description="Number of shares to trade")
    price: float = Field(gt=0, description="Price at which to execute the order")


class MarketOrderResponse(BaseModel):
    """API response for a submitted market order."""

    error: bool = Field(..., description="Indicates if there was an error")
    message: str = Field(..., description="Message describing the result")
    data: MarketOrderInput = Field(..., description="Data related to the market order")
