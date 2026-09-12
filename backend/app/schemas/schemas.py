"""
Pydantic schemas for request/response validation.
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from uuid import UUID


# ============ Authentication Schemas ============

class UserCreate(BaseModel):
    """Schema for user registration."""
    email: EmailStr
    password: str = Field(..., min_length=8)


class UserLogin(BaseModel):
    """Schema for user login."""
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """Schema for token response."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    """Schema for user data in responses."""
    id: UUID
    email: EmailStr
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


# ============ Portfolio Schemas ============

class PortfolioCreate(BaseModel):
    """Schema for creating a portfolio."""
    name: Optional[str] = "Main Portfolio"


class PortfolioResponse(BaseModel):
    """Schema for portfolio data."""
    id: UUID
    user_id: UUID
    name: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class HoldingCreate(BaseModel):
    """Schema for adding a holding."""
    symbol: str = Field(..., min_length=1, max_length=50)
    quantity: float = Field(..., gt=0)
    avg_price: float = Field(..., gt=0)


class HoldingUpdate(BaseModel):
    """Schema for updating a holding."""
    quantity: Optional[float] = None
    avg_price: Optional[float] = None


class HoldingResponse(BaseModel):
    """Schema for holding data with current price."""
    id: UUID
    portfolio_id: UUID
    symbol: str
    quantity: float
    avg_price: float
    current_price: Optional[float] = None
    current_value: Optional[float] = None
    pnl: Optional[float] = None
    pnl_percent: Optional[float] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ============ Watchlist Schemas ============

class WatchlistCreate(BaseModel):
    """Schema for creating a watchlist."""
    name: str = Field(..., min_length=1, max_length=100)


class WatchlistItemCreate(BaseModel):
    """Schema for adding item to watchlist."""
    symbol: str = Field(..., min_length=1, max_length=50)
    notes: Optional[str] = None


class WatchlistResponse(BaseModel):
    """Schema for watchlist with items."""
    id: UUID
    user_id: UUID
    name: str
    items: List[str] = []
    created_at: datetime
    
    class Config:
        from_attributes = True


# ============ Stock Data Schemas ============

class DailyPriceResponse(BaseModel):
    """Schema for daily price data."""
    symbol: str
    date: date
    open: Optional[float] = None
    high: Optional[float] = None
    low: Optional[float] = None
    close: Optional[float] = None
    volume: Optional[int] = None
    adjusted_close: Optional[float] = None


class StockQuote(BaseModel):
    """Schema for current stock quote."""
    symbol: str
    price: float
    change: Optional[float] = None
    change_percent: Optional[float] = None
    volume: Optional[int] = None
    market_cap: Optional[float] = None
    pe_ratio: Optional[float] = None
    timestamp: datetime
    source: Optional[str] = None
    is_mock: Optional[bool] = False


class StockFundamentals(BaseModel):
    """Schema for stock fundamental data."""
    symbol: str
    market_cap: Optional[float] = None
    pe_ratio: Optional[float] = None
    eps: Optional[float] = None
    book_value: Optional[float] = None
    debt_to_equity: Optional[float] = None
    roe: Optional[float] = None
    revenue_growth: Optional[float] = None
    profit_margin: Optional[float] = None


# ============ AI Chat Schemas ============

class ChatMessage(BaseModel):
    """Schema for chat message."""
    message: str
    conversation_id: Optional[UUID] = None


class ChatResponse(BaseModel):
    """Schema for AI chat response."""
    response: str
    conversation_id: UUID
    intent: Optional[str] = None
    entities: Optional[Dict[str, Any]] = None
    sources: Optional[List[str]] = None
    confidence: Optional[str] = None
    timestamp: datetime


class AnalysisRequest(BaseModel):
    """Schema for requesting stock analysis."""
    symbol: str
    time_horizon: str = Field(default="long_term", description="intraday, swing, positional, long_term")
    context: Optional[str] = None


class AnalysisReport(BaseModel):
    """Schema for structured analysis report."""
    symbol: str
    time_horizon: str
    business_overview: Optional[str] = None
    financial_performance: Optional[str] = None
    valuation: Optional[str] = None
    technical_position: Optional[str] = None
    catalysts: Optional[List[str]] = None
    risks: Optional[List[str]] = None
    conclusion: Optional[str] = None
    confidence_level: Optional[str] = None
    generated_at: datetime


# ============ Scanner Schemas ============

class ScanCriteria(BaseModel):
    """Schema for stock scanning criteria."""
    time_horizon: str = "long_term"
    min_market_cap: Optional[float] = None
    max_market_cap: Optional[float] = None
    min_pe_ratio: Optional[float] = None
    max_pe_ratio: Optional[float] = None
    min_roe: Optional[float] = None
    min_revenue_growth: Optional[float] = None
    min_profit_margin: Optional[float] = None
    technical_filters: Optional[Dict[str, Any]] = None


class ScanResult(BaseModel):
    """Schema for scan result item."""
    symbol: str
    score: float
    reasons: List[str]
    metrics: Dict[str, Any]


class ScanResponse(BaseModel):
    """Schema for complete scan response."""
    criteria: ScanCriteria
    results: List[ScanResult]
    total_scanned: int
    timestamp: datetime
