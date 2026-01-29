from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.repositories.vehicle_repository import VehicleRepository
from app.schemas.vehicle import VehicleCreateSchema
from app.core.database import get_db
from app.api.deps import get_current_user

router = APIRouter(tags=["Vehicles"], prefix="/vehicles")

@router.get("/")
def list_vehicles(db: Session = Depends(get_db)):
    return VehicleRepository.list_active(db)

@router.post("/")
def create_vehicle(payload: VehicleCreateSchema,
                   db: Session = Depends(get_db),
                   user=Depends(get_current_user)):
    return VehicleRepository.create(db, payload)
