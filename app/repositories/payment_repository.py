from sqlmodel import Session
from app.models.payment import Payment


class PaymentRepository:

    @staticmethod
    def create(db: Session, payment: Payment):
        db.add(payment)
        db.commit()
        db.refresh(payment)
        return payment
