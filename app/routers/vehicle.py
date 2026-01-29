from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.repositories.vehicle_repository import VehicleRepository
from app.schemas.vehicle import VehicleCreateSchema
from app.core.database import get_db
from typing import Optional
from datetime import date
from app.services.vehicle_service import VehicleService

router = APIRouter(tags=["Vehicles"], prefix="/vehicles")

@router.get("/")
def list_vehicles(db: Session = Depends(get_db)):
    return VehicleService.get_all_vehicles_with_status(db)

from app.api.deps import get_current_admin

@router.post("/")
def create_vehicle(payload: VehicleCreateSchema,
                   db: Session = Depends(get_db),
                   admin=Depends(get_current_admin)):
    
    return VehicleRepository.create(db, payload)
