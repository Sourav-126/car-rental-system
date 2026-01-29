from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import date
from enum import Enum

class BookingStatus(str, Enum):
    CONFIRMED = "CONFIRMED"
    CANCELLED = "CANCELLED"
    COMPLETED = "COMPLETED"

class PaymentStatus(str, Enum):
    UNPAID = "UNPAID"
    PAID = "PAID"

class Booking(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    user_id: int = Field(index=True, foreign_key="user.id")
    vehicle_id: int = Field(index=True, foreign_key="vehicles.id")

    start_date: date
    end_date: date

    status: BookingStatus = Field(default=BookingStatus.CONFIRMED)
    payment_status: PaymentStatus = Field(default=PaymentStatus.UNPAID)

    total_amount: float
    user: "User" = Relationship(back_populates="bookings")
    vehicle: "Vehicle" = Relationship(back_populates="bookings")
    payments: List["Payment"] = Relationship(back_populates="booking")
