"""
SQLAlchemy database models.
"""
from app.core.database import SessionLocal, engine
from .database_models import Base, User, Holding, Watchlist, WatchlistItem, Alert, ChatMessage

# Create all tables
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

__all__ = ["User", "Holding", "Watchlist", "WatchlistItem", "Alert", "ChatMessage", "get_db"]