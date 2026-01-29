from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app.core.database import get_db
from app.services.auth_service import AuthService
from app.schemas.user import UserCreateSchema, UserResponseSchema, UserLoginSchema
from app.schemas.auth import TokenSchema

router = APIRouter(tags=["Auth"], prefix="/auth")

@router.post("/signup", response_model=UserResponseSchema, status_code=status.HTTP_201_CREATED)
def signup(payload: UserCreateSchema, db: Session = Depends(get_db)):
    try:
        return AuthService.register(db, payload)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/login", response_model=TokenSchema)
def login(payload: UserLoginSchema, db: Session = Depends(get_db)):
    try:
        token = AuthService.login(db, payload.email, payload.password)
        return {"access_token": token, "token_type": "bearer"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )
