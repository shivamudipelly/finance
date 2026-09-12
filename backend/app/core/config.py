"""
Configuration settings for the application.
Loads from environment variables with sensible defaults.
"""
from pydantic_settings import BaseSettings
from typing import List, Optional
import os


class Settings(BaseSettings):
    # Application
    APP_NAME: str = "Market Intelligence Platform"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = True
    
    # Security
    SECRET_KEY: str = "change-this-secret-key-in-production-min-32-characters"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Database - Use SQLite for local development (zero cost, no setup)
    # In Docker, this will be overridden by environment variable to PostgreSQL
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./market_intelligence.db")
    
    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_URL: Optional[str] = None  # Full URL override for Docker
    
    # LLM Settings - Updated for Docker
    OLLAMA_BASE_URL: str = "http://ollama:11434"  # Docker service name
    OLLAMA_MODEL: str = "llama3.2"
    
    GROQ_API_KEY: Optional[str] = None
    GROQ_MODEL: str = "llama-3.2-90b-vision-preview"
    
    LLM_PROVIDER: str = "ollama"  # "ollama" or "groq"
    
    # Data Sources
    YFINANCE_ENABLED: bool = True
    ALPHA_VANTAGE_API_KEY: Optional[str] = None
    NSEPY_ENABLED: bool = True
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    RATE_LIMIT_PER_DAY: int = 1000
    
    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:5173", "http://localhost:3000"]
    
    # File Storage
    DATA_DIR: str = "./data"
    CACHE_DIR: str = "./cache"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

# Ensure directories exist
os.makedirs(settings.DATA_DIR, exist_ok=True)
os.makedirs(settings.CACHE_DIR, exist_ok=True)
