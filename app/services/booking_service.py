from datetime import date
from sqlmodel import Session
from app.models.booking import Booking, BookingStatus, PaymentStatus
from app.repositories.booking_repository import BookingRepository
from app.repositories.vehicle_repository import VehicleRepository
from app.services.payment_service import PaymentService


class BookingService:

    @staticmethod
    def create(db: Session, user, payload):
        if not user.is_verified:
            raise ValueError("KYC not verified")

        vehicle = VehicleRepository.get(db, payload.vehicle_id)
        if not vehicle:
            raise ValueError("Vehicle not found")

        today = date.today()
        if payload.start_date < today:
            raise ValueError("Cannot book a car for a past date")
        if payload.end_date < payload.start_date:
            raise ValueError("End date cannot be before start date")
        
        days = (payload.end_date - payload.start_date).days + 1
        if days > 7:
            raise ValueError("Cannot book a car for more than 7 days")

        conflict = BookingRepository.find_conflict(
            db,
            payload.vehicle_id,
            payload.start_date,
            payload.end_date
        )
        if conflict:
            raise ValueError("Vehicle not available in the requested period")

        days = (payload.end_date - payload.start_date).days + 1
        total_amount = days * vehicle.price_per_day

        booking = Booking(
            user_id=user.id,
            vehicle_id=vehicle.id,
            start_date=payload.start_date,
            end_date=payload.end_date,
            total_amount=total_amount,
            status=BookingStatus.CONFIRMED,
            payment_status=PaymentStatus.PAID
        )

        booking = BookingRepository.create(db, booking)

        PaymentService.pay(db, booking)
        
        db.commit()
        db.refresh(booking)

        return booking

    @staticmethod
    def cancel(db: Session, user, booking_id: int):
        
        booking = BookingRepository.get_by_id(db, booking_id)
        if not booking or booking.user_id != user.id:
            raise ValueError("Booking not found or not authorized")

        if booking.status == BookingStatus.CANCELLED:
            raise ValueError("Booking already cancelled")

        if booking.status == BookingStatus.COMPLETED:
            raise ValueError("Cannot cancel a completed booking")

        if booking.start_date <= date.today():
            raise ValueError("Cannot cancel a booking that has already started or is starting today")

        if booking.payment_status == PaymentStatus.PAID:
            PaymentService.refund(db, booking)

        booking.status = BookingStatus.CANCELLED
        db.add(booking)
        db.commit()
        db.refresh(booking)
        return booking

    @staticmethod
    def history(db: Session, user):
       
        return BookingRepository.user_bookings(db, user.id)
