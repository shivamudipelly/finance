"""
Portfolio management service.
"""
from typing import List, Optional, Dict, Any
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.tables import Portfolio, PortfolioStock, Watchlist, WatchlistStock
from app.schemas.schemas import PortfolioCreate, PortfolioStockCreate, PortfolioStockUpdate, WatchlistCreate, WatchlistStockCreate
from app.services.market_data import market_data_service


class PortfolioService:
    """Service for managing user portfolios."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_portfolio(self, user_id: UUID, data: PortfolioCreate) -> Portfolio:
        """Create a new portfolio."""
        portfolio = Portfolio(
            user_id=user_id,
            name=data.name
        )
        self.db.add(portfolio)
        self.db.commit()
        self.db.refresh(portfolio)
        return portfolio
    
    def get_portfolios(self, user_id: UUID) -> List[Portfolio]:
        """Get all portfolios for a user."""
        result = self.db.execute(
            select(Portfolio).where(Portfolio.user_id == user_id)
        )
        return list(result.scalars().all())
    
    def get_portfolio(self, portfolio_id: UUID, user_id: UUID) -> Optional[Portfolio]:
        """Get a specific portfolio."""
        result = self.db.execute(
            select(Portfolio).where(
                Portfolio.id == portfolio_id,
                Portfolio.user_id == user_id
            )
        )
        return result.scalar_one_or_none()
    
    def add_holding(self, portfolio_id: UUID, data: PortfolioStockCreate) -> PortfolioStock:
        """Add a holding to portfolio."""
        holding = PortfolioStock(
            portfolio_id=portfolio_id,
            ticker=data.ticker.upper(),
            quantity=data.quantity,
            average_price=data.average_price
        )
        self.db.add(holding)
        self.db.commit()
        self.db.refresh(holding)
        return holding
    
    def update_holding(self, holding_id: UUID, data: PortfolioStockUpdate) -> Optional[PortfolioStock]:
        """Update a holding."""
        holding = self.db.get(PortfolioStock, holding_id)
        if not holding:
            return None
        
        if data.quantity is not None:
            holding.quantity = data.quantity
        if data.average_price is not None:
            holding.average_price = data.average_price
        
        self.db.commit()
        self.db.refresh(holding)
        return holding
    
    def remove_holding(self, holding_id: UUID) -> bool:
        """Remove a holding from portfolio."""
        holding = self.db.get(PortfolioStock, holding_id)
        if not holding:
            return False
        
        self.db.delete(holding)
        self.db.commit()
        return True
    
    async def get_holdings_with_prices(self, portfolio_id: UUID) -> List[Dict[str, Any]]:
        """Get holdings with current prices and P&L."""
        result = self.db.execute(
            select(PortfolioStock).where(PortfolioStock.portfolio_id == portfolio_id)
        )
        holdings = list(result.scalars().all())
        
        holdings_data = []
        for holding in holdings:
            # Get current price
            quote = await market_data_service.get_current_quote(holding.ticker)
            current_price = quote.price if quote else None
            
            current_value = current_price * float(holding.quantity) if current_price else None
            cost_basis = float(holding.average_price) * float(holding.quantity)
            pnl = current_value - cost_basis if current_value else None
            pnl_percent = (pnl / cost_basis * 100) if pnl and cost_basis else None
            
            holdings_data.append({
                "id": str(holding.id),
                "portfolio_id": str(portfolio_id),
                "ticker": holding.ticker,
                "company_name": holding.company_name,
                "quantity": float(holding.quantity),
                "average_price": float(holding.average_price),
                "current_price": current_price,
                "current_value": current_value,
                "pnl": pnl,
                "pnl_percent": pnl_percent,
                "last_updated": holding.last_updated
            })
        
        return holdings_data
    
    async def get_portfolio_summary(self, portfolio_id: UUID) -> Dict[str, Any]:
        """Get portfolio summary with total value and P&L."""
        holdings = await self.get_holdings_with_prices(portfolio_id)
        
        total_value = sum(h.get("current_value", 0) or 0 for h in holdings)
        total_cost = sum(float(h["avg_price"]) * float(h["quantity"]) for h in holdings)
        total_pnl = total_value - total_cost
        total_pnl_percent = (total_pnl / total_cost * 100) if total_cost else 0
        
        return {
            "portfolio_id": str(portfolio_id),
            "total_value": total_value,
            "total_cost": total_cost,
            "total_pnl": total_pnl,
            "total_pnl_percent": round(total_pnl_percent, 2),
            "holdings_count": len(holdings),
            "holdings": holdings
        }


class WatchlistService:
    """Service for managing watchlists."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_watchlist(self, user_id: UUID, data: WatchlistCreate) -> Watchlist:
        """Create a new watchlist."""
        watchlist = Watchlist(
            user_id=user_id,
            name=data.name
        )
        self.db.add(watchlist)
        self.db.commit()
        self.db.refresh(watchlist)
        return watchlist
    
    def get_watchlists(self, user_id: UUID) -> List[Watchlist]:
        """Get all watchlists for a user."""
        result = self.db.execute(
            select(Watchlist).where(Watchlist.user_id == user_id)
        )
        return list(result.scalars().all())
    
    def add_to_watchlist(self, watchlist_id: UUID, data: WatchlistStockCreate) -> WatchlistStock:
        """Add item to watchlist."""
        item = WatchlistStock(
            watchlist_id=watchlist_id,
            ticker=data.ticker.upper(),
            notes=data.notes
        )
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item
    
    def remove_from_watchlist(self, watchlist_id: UUID, ticker: str) -> bool:
        """Remove item from watchlist."""
        result = self.db.execute(
            select(WatchlistStock).where(
                WatchlistStock.watchlist_id == watchlist_id,
                WatchlistStock.ticker == ticker.upper()
            )
        )
        item = result.scalar_one_or_none()
        
        if not item:
            return False
        
        self.db.delete(item)
        self.db.commit()
        return True
    
    async def get_watchlist_with_prices(self, watchlist_id: UUID) -> Dict[str, Any]:
        """Get watchlist with current prices."""
        result = self.db.execute(
            select(Watchlist).where(Watchlist.id == watchlist_id)
        )
        watchlist = result.scalar_one_or_none()
        
        if not watchlist:
            return {"error": "Watchlist not found"}
        
        # Get items
        items_result = self.db.execute(
            select(WatchlistStock).where(WatchlistStock.watchlist_id == watchlist_id)
        )
        items = list(items_result.scalars().all())
        
        # Get prices
        items_data = []
        for item in items:
            quote = await market_data_service.get_current_quote(item.ticker)
            items_data.append({
                "ticker": item.ticker,
                "company_name": item.company_name,
                "notes": item.notes,
                "price": quote.price if quote else None,
                "change": quote.change if quote else None,
                "change_percent": quote.change_percent if quote else None
            })
        
        return {
            "id": str(watchlist.id),
            "name": watchlist.name,
            "items": items_data
        }
