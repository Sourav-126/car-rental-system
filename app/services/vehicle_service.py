from sqlmodel import Session, select
from app.models.vehicle import Vehicle
from app.models.booking import Booking, BookingStatus
from datetime import date

class VehicleService:

    @staticmethod
    def get_available_vehicles(db: Session, start_date: date, end_date: date):
        conflicting_bookings = select(Booking.vehicle_id).where(
            Booking.status == BookingStatus.CONFIRMED,
            Booking.start_date < end_date,
            Booking.end_date > start_date
        )
        
        available_vehicles = db.exec(
            select(Vehicle).where(
                Vehicle.is_active == True,
                ~Vehicle.id.in_(conflicting_bookings)
            )
        ).all()
        
        return available_vehicles
    @staticmethod
    def get_all_vehicles_with_status(db: Session):
        vehicles = db.exec(select(Vehicle).where(Vehicle.is_active == True)).all()
        result = []
        today = date.today()
        
        for v in vehicles:
            active_booking = db.exec(
                select(Booking)
                .where(
                    Booking.vehicle_id == v.id,
                    Booking.status == BookingStatus.CONFIRMED,
                    Booking.start_date <= today,
                    Booking.end_date >= today
                )
            ).first()
            
            latest_booking = db.exec(
                select(Booking)
                .where(
                    Booking.vehicle_id == v.id,
                    Booking.status == BookingStatus.CONFIRMED,
                    Booking.end_date >= today
                )
                .order_by(Booking.end_date.desc())
            ).first()
            
            available_from = None
            if active_booking:
                available_from = str(active_booking.end_date)
            
            result.append({
                "id": v.id,
                "brand": v.brand,
                "model": v.model,
                "vehicle_type": v.vehicle_type,
                "price_per_day": v.price_per_day,
                "is_active": v.is_active,
                "is_currently_booked": active_booking is not None,
                "available_from": available_from
            })
            
        return result
