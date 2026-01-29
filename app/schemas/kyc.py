from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class KYCSubmitSchema(BaseModel):
    document_type: str
    document_number: str
    email: EmailStr
    phone_number: str


class KYCVerifyOTPSchema(BaseModel):
    email: EmailStr
    otp: str


class KYCResponseSchema(BaseModel):
    id: int
    user_id: int
    document_type: str
    document_number: str
    email: EmailStr
    status: str
    verified_at: Optional[datetime]

    class Config:
        from_attributes = True
