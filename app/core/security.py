import hashlib
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    pw_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
    return pwd_context.hash(pw_hash)


def verify_password(password: str, hashed: str) -> bool:
    pw_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
    return pwd_context.verify(pw_hash, hashed)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})

    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm="HS256"
    )
