from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime


class Payment(SQLModel, table=True):
    __tablename__ = "payments"

    id: Optional[int] = Field(default=None, primary_key=True)

    booking_id: int = Field(index=True, foreign_key="booking.id")
    user_id: int = Field(index=True, foreign_key="user.id")
    vehicle_id: int = Field(index=True, foreign_key="vehicles.id")
    
    amount: float

    status: str 
    transaction_id: str
    
    is_refunded: bool = Field(default=False)
    refund_id: Optional[str] = Field(default=None)

    created_at: datetime = Field(default_factory=datetime.utcnow)

    booking: "Booking" = Relationship(back_populates="payments")
    user: "User" = Relationship(back_populates="payments")
