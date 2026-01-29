from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserCreateSchema(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserUpdateSchema(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str




class UserResponseSchema(BaseModel):
    id: int
    name: str
    email: EmailStr
    is_verified: bool
    role: str
    created_at: datetime

    class Config:
        from_attributes = True
