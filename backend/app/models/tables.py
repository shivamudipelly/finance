"""
SQLAlchemy database models.
"""
from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, DECIMAL, BigInteger, Text, JSONB, Date, PrimaryKeyConstraint
from sqlalchemy.dialects.postgresql import UUID, JSON
from sqlalchemy.sql import func
from app.core.database import Base


class User(Base):
    """User account model."""
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=func.gen_random_uuid())
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_login = Column(DateTime(timezone=True))
    is_active = Column(Boolean, default=True)


class Portfolio(Base):
    """User portfolio model."""
    __tablename__ = "portfolios"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=func.gen_random_uuid())
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    name = Column(String(100), default="Main Portfolio")
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Holding(Base):
    """Portfolio holding model."""
    __tablename__ = "holdings"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=func.gen_random_uuid())
    portfolio_id = Column(UUID(as_uuid=True), ForeignKey("portfolios.id"), nullable=False, index=True)
    symbol = Column(String(50), nullable=False)
    quantity = Column(DECIMAL, nullable=False)
    avg_price = Column(DECIMAL, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class Watchlist(Base):
    """User watchlist model."""
    __tablename__ = "watchlists"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=func.gen_random_uuid())
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    name = Column(String(100), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class WatchlistItem(Base):
    """Watchlist item model."""
    __tablename__ = "watchlist_items"
    
    watchlist_id = Column(UUID(as_uuid=True), ForeignKey("watchlists.id"), primary_key=True)
    symbol = Column(String(50), primary_key=True)
    added_at = Column(DateTime(timezone=True), server_default=func.now())
    notes = Column(Text)


class DailyPrice(Base):
    """Daily stock price data."""
    __tablename__ = "daily_prices"
    
    symbol = Column(String(50), primary_key=True)
    date = Column(Date, primary_key=True)
    open = Column(DECIMAL)
    high = Column(DECIMAL)
    low = Column(DECIMAL)
    close = Column(DECIMAL)
    volume = Column(BigInteger)
    adjusted_close = Column(DECIMAL)
    
    __table_args__ = (
        # Index for efficient querying by symbol and date descending
        {'extend_existing': True}
    )


class Fundamental(Base):
    """Company fundamental data (quarterly snapshots)."""
    __tablename__ = "fundamentals"
    
    symbol = Column(String(50), primary_key=True)
    report_date = Column(Date, primary_key=True)
    filing_date = Column(Date)
    revenue = Column(DECIMAL)
    net_income = Column(DECIMAL)
    eps = Column(DECIMAL)
    book_value = Column(DECIMAL)
    total_debt = Column(DECIMAL)
    cash_and_equivalents = Column(DECIMAL)
    operating_cash_flow = Column(DECIMAL)
    shares_outstanding = Column(BigInteger)


class Conversation(Base):
    """AI conversation model."""
    __tablename__ = "conversations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=func.gen_random_uuid())
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Message(Base):
    """Conversation message model."""
    __tablename__ = "messages"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=func.gen_random_uuid())
    conversation_id = Column(UUID(as_uuid=True), ForeignKey("conversations.id"), nullable=False, index=True)
    role = Column(String(20), nullable=False)  # 'user' or 'assistant'
    content = Column(Text, nullable=False)
    metadata = Column(JSON)  # Store intent, entities, sources
    created_at = Column(DateTime(timezone=True), server_default=func.now())
