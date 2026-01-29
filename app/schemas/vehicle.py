from pydantic import BaseModel
from typing import Optional


class VehicleCreateSchema(BaseModel):
    brand: str
    model: str
    vehicle_type: str
    price_per_day: float


class VehicleUpdateSchema(BaseModel):
    brand: Optional[str]
    model: Optional[str]
    vehicle_type: Optional[str]
    price_per_day: Optional[float]
    is_active: Optional[bool]


class VehicleResponseSchema(BaseModel):
    id: int
    brand: str
    model: str
    vehicle_type: str
    price_per_day: float
    is_active: bool

    class Config:
        from_attributes = True

class VehicleCreateSchema(BaseModel):
    brand: str
    model: str
    vehicle_type: str
    price_per_day: float