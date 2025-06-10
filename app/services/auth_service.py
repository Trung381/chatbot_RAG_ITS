from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import create_access_token
from app.models.user import User
from .user_service import UserService


class AuthService:
    def __init__(self):
        self.user_service = UserService()

    def authenticate_user(
        self, db: Session, *, email: str, password: str
    ) -> Optional[User]:
        """
        Authenticate a user by email and password
        """
        return self.user_service.authenticate(db, email=email, password=password)

    def create_access_token(self, user_id: int) -> str:
        """
        Create access token for user
        """
        expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        return create_access_token(user_id, expires_delta=expires_delta)
        
    def register_new_user(self, db: Session, *, email: str, username: str, password: str, full_name: Optional[str] = None) -> User:
        """
        Register a new user
        """
        # Check if user exists
        existing_user = self.user_service.get_by_email(db, email=email)
        if existing_user:
            return None
            
        # Create user object
        user_in = {
            "email": email,
            "username": username,
            "password": password,
            "full_name": full_name,
            "is_active": True,
            "is_superuser": False
        }
        
        # Create user
        return self.user_service.create(db, obj_in=user_in)
