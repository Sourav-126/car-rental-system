from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.core.database import get_db
from app.api.deps import get_current_admin
from app.models.vehicle import Vehicle
from app.models.booking import Booking, BookingStatus
from app.models.user import User
from app.schemas.vehicle import VehicleCreateSchema, VehicleResponseSchema
from app.repositories.vehicle_repository import VehicleRepository

router = APIRouter(tags=["Admin"], prefix="/admin")

@router.post("/vehicles/", response_model=VehicleResponseSchema)
def create_vehicle(payload: VehicleCreateSchema, 
                   db: Session = Depends(get_db), 
                   admin: User = Depends(get_current_admin)):
    vehicle = Vehicle(**payload.dict())
    return VehicleRepository.create(db, vehicle)

@router.delete("/vehicles/{vehicle_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_vehicle(vehicle_id: int, 
                   db: Session = Depends(get_db), 
                   admin: User = Depends(get_current_admin)):
    vehicle = VehicleRepository.get(db, vehicle_id)
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    VehicleRepository.delete(db, vehicle)
    return None

@router.get("/vehicles/")
def list_admin_vehicles(db: Session = Depends(get_db), 
                        admin: User = Depends(get_current_admin)):
    vehicles = VehicleRepository.list_all(db)
    result = []
    
    for v in vehicles:
      
        bookings = db.exec(
            select(Booking, User)
            .where(Booking.vehicle_id == v.id)
            .join(User, Booking.user_id == User.id)
        ).all()
        
        booking_details = []
        is_free = True
        for b, u in bookings:
            if b.status == BookingStatus.CONFIRMED:
                is_free = False
            
            booking_details.append({
                "user_name": u.name,
                "user_email": u.email,
                "status": b.status,
                "payment_status": b.payment_status,
                "start_date": b.start_date,
                "end_date": b.end_date
            })
        
        result.append({
            "id": v.id,
            "brand": v.brand,
            "model": v.model,
            "vehicle_type": v.vehicle_type,
            "price_per_day": v.price_per_day,
            "is_active": v.is_active,
            "is_free": is_free,
            "bookings": booking_details
        })
        
    return result
