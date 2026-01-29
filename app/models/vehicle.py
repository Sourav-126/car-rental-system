from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List


class Vehicle(SQLModel, table=True):
    __tablename__ = "vehicles"

    id: Optional[int] = Field(default=None, primary_key=True)

    brand: str
    model: str
    vehicle_type: str

    price_per_day: float
    is_active: bool = Field(default=True)

    bookings: List["Booking"] = Relationship(back_populates="vehicle")
