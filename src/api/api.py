"""FastAPI routes for users, portfolios, and market orders."""

from fastapi import APIRouter, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from api.schemas import (
    PortfolioIdResponse,
    UserIdResponse,
)
from services.portfolio_service import PortfolioService
from services.user_service import UserService

app = FastAPI(
    title="Backend API",
    description="Backend API for My Application",
    version="1.0.0",
    debug=True,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)


user_router = APIRouter(prefix="/api/v1/users")
portfolio_router = APIRouter(prefix="/api/v1/portfolios")
bot_router = APIRouter(prefix="/api/v1/bots")
trading_router = APIRouter(prefix="/api/v1/trading")


@user_router.get(
    "/{user_name}", status_code=200, tags=["Users"], response_model=UserIdResponse
)
def get_user(user_name: str) -> UserIdResponse:
    try:
        user_id = UserService().get_user_id(user_name)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail="User not found") from exc

    return UserIdResponse(
        error=False,
        message="User retrieved successfully",
        user_id=user_id,
    )


@user_router.post(
    "/{user_name}", status_code=200, tags=["Users"], response_model=UserIdResponse
)
def create_user(user_name: str) -> UserIdResponse:
    try:
        user_id = UserService().create_user(user_name)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail="User not found") from exc

    return UserIdResponse(
        error=False,
        message="User created successfully",
        user_id=user_id,
    )


@portfolio_router.get(
    "/{user_id}/{portfolio_name}",
    status_code=200,
    tags=["Portfolios"],
    response_model=PortfolioIdResponse,
)
def get_portfolio(user_id: int, portfolio_name: str) -> PortfolioIdResponse:
    try:
        portfolio_id = PortfolioService().get_portfolio_id(user_id, portfolio_name)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail="Portfolio not found") from exc

    return PortfolioIdResponse(
        error=False,
        message="Portfolio retrieved successfully",
        portfolio_id=portfolio_id,
    )


@portfolio_router.post(
    "/{user_id}/{portfolio_name}/{cash}",
    status_code=200,
    tags=["Portfolios"],
    response_model=PortfolioIdResponse,
)
def create_portfolio(
    user_id: int, portfolio_name: str, cash: float
) -> PortfolioIdResponse:
    try:
        portfolio_id = PortfolioService().create_portfolio(
            user_id, portfolio_name, cash
        )
    except ValueError as exc:
        raise HTTPException(status_code=404, detail="Portfolio not found") from exc

    return PortfolioIdResponse(
        error=False,
        message="Portfolio created successfully",
        portfolio_id=portfolio_id,
    )


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT"],
    allow_headers=["x-apigateway-header", "Content-Type", "X-Amz-Date"],
)
app.include_router(user_router)
app.include_router(portfolio_router)
app.include_router(bot_router)
app.include_router(trading_router)
