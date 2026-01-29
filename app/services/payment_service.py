import uuid
from app.models.payment import Payment
from app.repositories.payment_repository import PaymentRepository

class PaymentService:

    @staticmethod
    def pay(db, booking):
        payment = Payment(
            booking_id=booking.id,
            user_id=booking.user_id,
            vehicle_id=booking.vehicle_id,
            amount=booking.total_amount,
            status="SUCCESS",
            transaction_id=str(uuid.uuid4())
        )
        return PaymentRepository.create(db, payment)

    @staticmethod
    def refund(db, booking):
        from sqlmodel import select
        payments = db.exec(select(Payment).where(Payment.booking_id == booking.id)).all()
        for p in payments:
            p.status = "REFUNDED"
            p.is_refunded = True
            p.refund_id = f"REF-{uuid.uuid4().hex[:8].upper()}"
            db.add(p)
