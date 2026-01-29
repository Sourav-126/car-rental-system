from sqlmodel import Session, select
from app.models.booking import Booking, BookingStatus

class BookingRepository:

    @staticmethod
    def find_conflict(db: Session, vehicle_id: int, start_date, end_date):
        return db.exec(
            select(Booking).where(
                Booking.vehicle_id == vehicle_id,
                Booking.status == BookingStatus.CONFIRMED,
                Booking.start_date <= end_date,
                Booking.end_date >= start_date
            )
        ).first()

    @staticmethod
    def create(db: Session, booking: Booking):
        db.add(booking)
        db.commit()
        db.refresh(booking)
        return booking

    @staticmethod
    def get_by_id(db: Session, booking_id: int):
        return db.get(Booking, booking_id)

    @staticmethod
    def user_bookings(db: Session, user_id: int):
        return db.exec(
            select(Booking).where(Booking.user_id == user_id)
        ).all()
