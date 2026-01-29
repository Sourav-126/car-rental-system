from pydantic import BaseModel
from datetime import date
from typing import Optional


class BookingCreateSchema(BaseModel):
    vehicle_id: int
    start_date: date
    end_date: date


class BookingCancelSchema(BaseModel):
    reason: Optional[str]


class BookingResponseSchema(BaseModel):
    id: int
    user_id: int
    vehicle_id: int
    start_date: date
    end_date: date
    status: str
    payment_status: str
    total_amount: float

    class Config:
        from_attributes = True
