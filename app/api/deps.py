from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from sqlmodel import Session
from app.core.config import settings
from app.core.database import get_db
from app.repositories.user_repository import UserRepository
from app.models.user import User

security = HTTPBearer()

def get_current_user(auth: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)) -> User:
    token = auth.credentials
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
        
    user = UserRepository.get_by_id(db, int(user_id))
    if user is None:
        raise credentials_exception
    return user

def get_current_admin(user: User = Depends(get_current_user)) -> User:
    if user.role != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges",
        )
    return user
