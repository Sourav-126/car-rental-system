from sqlmodel import Session, select
from app.models.kyc import KYC


class KYCRepository:

    @staticmethod
    def create(db: Session, kyc: KYC):
        db.add(kyc)
        db.commit()
        db.refresh(kyc)
        return kyc

    @staticmethod
    def get_by_email(db: Session, email: str):
        statement = select(KYC).where(KYC.email == email)
        return db.exec(statement).first()
