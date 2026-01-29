from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from datetime import datetime

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    email: str = Field(unique=True, index=True)
    name: str
    hashed_password: str
    role: str = Field(default="USER")

    is_verified: bool = Field(default=False)

    created_at: datetime = Field(default_factory=datetime.utcnow)

    kyc: Optional["KYC"] = Relationship(back_populates="user")
    bookings: List["Booking"] = Relationship(back_populates="user")
    payments: List["Payment"] = Relationship(back_populates="user")
