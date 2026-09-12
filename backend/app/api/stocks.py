"""
Stock data API routes.
"""
from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional

from app.services.market_data import market_data_service
from app.schemas.schemas import DailyPriceResponse, StockQuote, StockFundamentals

router = APIRouter()


@router.get("/search")
async def search_stocks(q: str):
    """Search for stocks by symbol or name."""
    results = await market_data_service.search_stocks(q)
    return {"results": results}


@router.get("/{symbol}/quote", response_model=StockQuote)
async def get_quote(symbol: str):
    """Get current stock quote."""
    quote = await market_data_service.get_current_quote(symbol)
    if not quote:
        raise HTTPException(status_code=404, detail="Stock not found or data unavailable")
    return quote


@router.get("/{symbol}/fundamentals", response_model=StockFundamentals)
async def get_fundamentals(symbol: str):
    """Get stock fundamental data."""
    fundamentals = await market_data_service.get_fundamentals(symbol)
    if not fundamentals:
        raise HTTPException(status_code=404, detail="Fundamental data not available")
    return fundamentals


@router.get("/{symbol}/prices", response_model=List[DailyPriceResponse])
async def get_historical_prices(
    symbol: str,
    period: str = "1y"
):
    """Get historical daily prices."""
    prices = await market_data_service.get_historical_prices(symbol, period=period)
    if not prices:
        raise HTTPException(status_code=404, detail="Price data not available")
    return prices


@router.get("/{symbol}/company")
async def get_company_info(symbol: str):
    """Get company information."""
    info = await market_data_service.get_company_info(symbol)
    if not info:
        raise HTTPException(status_code=404, detail="Company information not available")
    return info
