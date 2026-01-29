from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional


class KYC(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    user_id: int = Field(index=True, foreign_key="user.id", unique=True)

    document_type: str
    document_number: str

    email: str = Field(index=True)
    phone_number: str

    status: str = Field(default="PENDING", index=True)

    verified_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    user: Optional["User"] = Relationship(back_populates="kyc")
