"""
Authentication service.
"""
from datetime import timedelta
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.tables import User
from app.schemas.schemas import UserCreate, UserLogin
from app.core.security import verify_password, get_password_hash, create_access_token, create_refresh_token, decode_token


class AuthService:
    """Service for user authentication."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def register_user(self, data: UserCreate) -> Optional[User]:
        """Register a new user."""
        # Check if user already exists
        existing = self.db.execute(
            select(User).where(User.email == data.email)
        ).scalar_one_or_none()
        
        if existing:
            return None
        
        # Create new user
        user = User(
            email=data.email,
            password_hash=get_password_hash(data.password)
        )
        
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def authenticate_user(self, data: UserLogin) -> Optional[User]:
        """Authenticate user and return user object if successful."""
        user = self.db.execute(
            select(User).where(User.email == data.email)
        ).scalar_one_or_none()
        
        if not user:
            return None
        
        if not verify_password(data.password, user.password_hash):
            return None
        
        return user
    
    def create_tokens(self, user: User) -> dict:
        """Create access and refresh tokens for a user."""
        access_token = create_access_token(
            data={"sub": str(user.id), "type": "access"}
        )
        refresh_token = create_refresh_token(
            data={"sub": str(user.id), "type": "refresh"}
        )
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }
    
    def get_user_from_token(self, token: str) -> Optional[User]:
        """Get user from JWT token."""
        payload = decode_token(token)
        
        if not payload or payload.get("type") != "access":
            return None
        
        user_id = payload.get("sub")
        if not user_id:
            return None
        
        user = self.db.get(User, user_id)
        return user
    
    def refresh_access_token(self, refresh_token: str) -> Optional[str]:
        """Generate new access token from refresh token."""
        payload = decode_token(refresh_token)
        
        if not payload or payload.get("type") != "refresh":
            return None
        
        user_id = payload.get("sub")
        if not user_id:
            return None
        
        user = self.db.get(User, user_id)
        if not user or not user.is_active:
            return None
        
        return create_access_token(
            data={"sub": str(user.id), "type": "access"}
        )
