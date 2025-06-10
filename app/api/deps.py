from typing import Generator
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.redis import get_redis
from app.core.security import verify_token
from app.models.user import User
from app.core.exceptions import AuthenticationError
from app.services.user_service import UserService

security = HTTPBearer()
user_service = UserService()

def get_current_user(
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> User:
    token = credentials.credentials
    payload = verify_token(token)
    if payload is None:
        raise AuthenticationError("Could not validate credentials")
    
    user = user_service.get(db, id=payload.get("sub"))
    if user is None:
        raise AuthenticationError("User not found")
    
    if not user_service.is_active(user):
        raise AuthenticationError("Inactive user")
    
    return user

def get_current_active_superuser(
    current_user: User = Depends(get_current_user),
) -> User:
    if not user_service.is_superuser(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges"
        )
    return current_user
