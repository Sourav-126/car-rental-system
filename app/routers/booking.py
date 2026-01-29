from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.schemas.booking import BookingCreateSchema
from app.services.booking_service import BookingService
from app.core.database import get_db
from app.api.deps import get_current_user

router = APIRouter(tags=["Bookings"], prefix="/bookings")


@router.post("/")
def book(payload: BookingCreateSchema,
         db: Session = Depends(get_db),
         user=Depends(get_current_user)):
    """
    Create a booking:
    - Checks KYC verified
    - Checks vehicle exists
    - Checks booking conflict
    - Calculates total amount
    - Processes dummy payment
    """
    try:
        return BookingService.create(db, user, payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/cancel/{booking_id}")
def cancel_booking(booking_id: int,
                   db: Session = Depends(get_db),
                   user=Depends(get_current_user)):
    """
    Cancel a booking:
    - Only the booking owner can cancel
    - Booking status set to CANCELLED
    - Vehicle becomes available immediately
    """
    try:
        return BookingService.cancel(db, user, booking_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/me")
def my_bookings(db: Session = Depends(get_db),
                user=Depends(get_current_user)):
    """
    Get all bookings for the logged-in user
    """
    return BookingService.history(db, user)
