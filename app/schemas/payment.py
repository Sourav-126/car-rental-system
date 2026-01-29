from pydantic import BaseModel
from datetime import datetime


class PaymentResponseSchema(BaseModel):
    id: int
    booking_id: int
    amount: float
    status: str
    transaction_id: str
    created_at: datetime

    class Config:
        from_attributes = True
