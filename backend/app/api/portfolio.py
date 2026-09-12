"""
Portfolio API routes.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.api.auth import get_current_user
from app.models.tables import User
from app.schemas.schemas import (
    PortfolioCreate, PortfolioResponse, 
    PortfolioStockCreate, PortfolioStockUpdate,
    WatchlistCreate, WatchlistStockCreate
)
from app.services.portfolio import PortfolioService, WatchlistService

router = APIRouter()


def get_portfolio_service(db: Session = Depends(get_db)):
    return PortfolioService(db)


def get_watchlist_service(db: Session = Depends(get_db)):
    return WatchlistService(db)


# ============ Portfolio Routes ============

@router.post("/portfolios", response_model=PortfolioResponse)
async def create_portfolio(
    data: PortfolioCreate,
    current_user: User = Depends(get_current_user),
    service: PortfolioService = Depends(get_portfolio_service)
):
    """Create a new portfolio."""
    portfolio = service.create_portfolio(current_user.id, data)
    return portfolio


@router.get("/portfolios", response_model=List[PortfolioResponse])
async def get_portfolios(
    current_user: User = Depends(get_current_user),
    service: PortfolioService = Depends(get_portfolio_service)
):
    """Get all portfolios for current user."""
    return service.get_portfolios(current_user.id)


@router.post("/portfolios/{portfolio_id}/holdings")
async def add_holding(
    portfolio_id: str,
    data: PortfolioStockCreate,
    current_user: User = Depends(get_current_user),
    service: PortfolioService = Depends(get_portfolio_service)
):
    """Add a holding to portfolio."""
    from uuid import UUID
    try:
        holding = service.add_holding(UUID(portfolio_id), data)
        return {"message": "Holding added", "holding_id": str(holding.id)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/portfolios/{portfolio_id}/holdings")
async def get_holdings(
    portfolio_id: str,
    current_user: User = Depends(get_current_user),
    service: PortfolioService = Depends(get_portfolio_service)
):
    """Get all holdings in a portfolio with current prices."""
    from uuid import UUID
    try:
        holdings = await service.get_holdings_with_prices(UUID(portfolio_id))
        return {"holdings": holdings}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/portfolios/{portfolio_id}/summary")
async def get_portfolio_summary(
    portfolio_id: str,
    current_user: User = Depends(get_current_user),
    service: PortfolioService = Depends(get_portfolio_service)
):
    """Get portfolio summary with total value and P&L."""
    from uuid import UUID
    try:
        summary = await service.get_portfolio_summary(UUID(portfolio_id))
        return summary
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/holdings/{holding_id}")
async def remove_holding(
    holding_id: str,
    current_user: User = Depends(get_current_user),
    service: PortfolioService = Depends(get_portfolio_service)
):
    """Remove a holding from portfolio."""
    from uuid import UUID
    try:
        success = service.remove_holding(UUID(holding_id))
        if not success:
            raise HTTPException(status_code=404, detail="Holding not found")
        return {"message": "Holding removed"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============ Watchlist Routes ============

@router.post("/watchlists")
async def create_watchlist(
    data: WatchlistCreate,
    current_user: User = Depends(get_current_user),
    service: WatchlistService = Depends(get_watchlist_service)
):
    """Create a new watchlist."""
    watchlist = service.create_watchlist(current_user.id, data)
    return {"message": "Watchlist created", "watchlist_id": str(watchlist.id)}


@router.get("/watchlists")
async def get_watchlists(
    current_user: User = Depends(get_current_user),
    service: WatchlistService = Depends(get_watchlist_service)
):
    """Get all watchlists for current user."""
    watchlists = service.get_watchlists(current_user.id)
    return {
        "watchlists": [
            {"id": str(w.id), "name": w.name, "created_at": w.created_at}
            for w in watchlists
        ]
    }


@router.post("/watchlists/{watchlist_id}/items")
async def add_to_watchlist(
    watchlist_id: str,
    data: WatchlistStockCreate,
    current_user: User = Depends(get_current_user),
    service: WatchlistService = Depends(get_watchlist_service)
):
    """Add item to watchlist."""
    from uuid import UUID
    try:
        item = service.add_to_watchlist(UUID(watchlist_id), data)
        return {"message": "Item added", "item_id": str(item.id)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/watchlists/{watchlist_id}")
async def get_watchlist(
    watchlist_id: str,
    current_user: User = Depends(get_current_user),
    service: WatchlistService = Depends(get_watchlist_service)
):
    """Get watchlist with current prices."""
    from uuid import UUID
    try:
        watchlist = await service.get_watchlist_with_prices(UUID(watchlist_id))
        return watchlist
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/watchlists/{watchlist_id}/items/{ticker}")
async def remove_from_watchlist(
    watchlist_id: str,
    ticker: str,
    current_user: User = Depends(get_current_user),
    service: WatchlistService = Depends(get_watchlist_service)
):
    """Remove item from watchlist."""
    from uuid import UUID
    try:
        success = service.remove_from_watchlist(UUID(watchlist_id), ticker)
        if not success:
            raise HTTPException(status_code=404, detail="Item not found in watchlist")
        return {"message": "Item removed"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
