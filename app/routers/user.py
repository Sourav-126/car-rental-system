from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.core.database import get_db
from app.api.deps import get_current_user
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserResponseSchema, UserUpdateSchema

router = APIRouter(tags=["Users"], prefix="/users")

@router.get("/me", response_model=UserResponseSchema)
def get_me(user=Depends(get_current_user)):
    return user

@router.put("/me", response_model=UserResponseSchema)
def update_me(payload: UserUpdateSchema, 
              db: Session = Depends(get_db), 
              user=Depends(get_current_user)):
    if payload.name:
        user.name = payload.name
    if payload.email:
        
        if payload.email != user.email:
            existing = UserRepository.get_by_email(db, payload.email)
            if existing:
                raise HTTPException(status_code=400, detail="Email already taken")
            user.email = payload.email
            
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
