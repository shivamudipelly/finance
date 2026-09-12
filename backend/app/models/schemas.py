from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

# User schemas
class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str
    full_name: Optional[str] = None

class UserLogin(BaseModel):
    email: str
    password: str

class UserResponse(UserBase):
    id: int
    full_name: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

# Token schema
class Token(BaseModel):
    access_token: str
    token_type: str

# Portfolio schemas
class HoldingBase(BaseModel):
    ticker: str
    quantity: float
    avg_price: float
    notes: Optional[str] = None

class HoldingCreate(HoldingBase):
    pass

class HoldingResponse(HoldingBase):
    id: int
    user_id: int
    current_price: Optional[float] = None
    current_value: Optional[float] = None
    invested_value: Optional[float] = None
    pnl: Optional[float] = None
    pnl_percent: Optional[float] = None
    updated_at: datetime
    
    class Config:
        from_attributes = True

class PortfolioSummary(BaseModel):
    total_invested: float
    total_current_value: float
    total_pnl: float
    total_pnl_percent: float
    holdings_count: int
    top_gainers: List[Dict[str, Any]]
    top_losers: List[Dict[str, Any]]

# Watchlist schemas
class WatchlistBase(BaseModel):
    name: str
    description: Optional[str] = None

class WatchlistCreate(WatchlistBase):
    pass

class WatchlistResponse(WatchlistBase):
    id: int
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class WatchlistItemBase(BaseModel):
    ticker: str
    notes: Optional[str] = None

class WatchlistItemCreate(WatchlistItemBase):
    watchlist_id: int

class WatchlistItemResponse(WatchlistItemBase):
    id: int
    watchlist_id: int
    current_price: Optional[float] = None
    change_percent: Optional[float] = None
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Chat schemas
class ChatMessage(BaseModel):
    role: str  # 'user' or 'assistant'
    content: str

class ChatRequest(BaseModel):
    message: str
    context: Optional[List[ChatMessage]] = None
    user_intent: Optional[str] = None  # Optional override for intent

class ChatResponse(BaseModel):
    response: str
    intent: str
    tickers_mentioned: List[str]
    timeframe: str
    confidence: float
    sources: List[str]
    is_mock_data: bool = False
    warnings: List[str] = []

# Market data schemas
class QuoteData(BaseModel):
    ticker: str
    name: Optional[str] = None
    price: float
    change: float
    change_percent: float
    open: Optional[float] = None
    high: Optional[float] = None
    low: Optional[float] = None
    previous_close: Optional[float] = None
    volume: Optional[int] = None
    market_cap: Optional[float] = None
    pe_ratio: Optional[float] = None
    source: str
    is_mock: bool = False
    timestamp: datetime

class HistoricalDataPoint(BaseModel):
    date: datetime
    open: float
    high: float
    low: float
    close: float
    volume: int
    adjusted_close: Optional[float] = None

class HistoricalDataResponse(BaseModel):
    ticker: str
    data: List[HistoricalDataPoint]
    source: str
    is_mock: bool = False

# Scanner schemas
class ScanRequest(BaseModel):
    scan_type: str  # 'long_term', 'swing', 'value', 'momentum'
    sector: Optional[str] = None
    min_market_cap: Optional[float] = None
    max_pe: Optional[float] = None
    min_volume: Optional[int] = None
    limit: int = 20

class ScanResult(BaseModel):
    ticker: str
    name: Optional[str] = None
    score: float
    price: float
    change_percent: float
    market_cap: Optional[float] = None
    pe_ratio: Optional[float] = None
    reasons: List[str]
    risks: List[str]
    source: str
    is_mock: bool = False

# IPO schemas
class IPOInfo(BaseModel):
    company_name: str
    issue_size: Optional[float] = None
    price_band_low: Optional[float] = None
    price_band_high: Optional[float] = None
    open_date: Optional[str] = None
    close_date: Optional[str] = None
    listing_date: Optional[str] = None
    fresh_issue: Optional[float] = None
    ofs: Optional[float] = None
    pe_ratio: Optional[float] = None
    industry_pe: Optional[float] = None
    subscription_status: Optional[str] = None
    grey_market_premium: Optional[float] = None
    analyst_recommendation: Optional[str] = None
    risks: List[str] = []
    strengths: List[str] = []

# Alert schemas
class AlertBase(BaseModel):
    ticker: str
    alert_type: str  # 'price_above', 'price_below', 'volume_spike', 'news'
    threshold: Optional[float] = None
    message: Optional[str] = None
    is_active: bool = True

class AlertCreate(AlertBase):
    pass

class AlertResponse(AlertBase):
    id: int
    user_id: int
    triggered_at: Optional[datetime] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

# Dashboard schemas
class MarketOverview(BaseModel):
    nifty50: Optional[QuoteData] = None
    bank_nifty: Optional[QuoteData] = None
    sensex: Optional[QuoteData] = None
    market_breadth: Optional[Dict[str, Any]] = None
    sector_performance: List[Dict[str, Any]] = []
    top_movers: List[Dict[str, Any]] = []
    is_mock_data: bool = False

class DashboardResponse(BaseModel):
    market_overview: MarketOverview
    portfolio_summary: Optional[PortfolioSummary] = None
    watchlist_updates: List[Dict[str, Any]] = []
    recent_alerts: List[Dict[str, Any]] = []
    ai_insights: List[str] = []
