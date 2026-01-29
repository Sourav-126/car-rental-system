from sqlmodel import Session, select
from app.models.user import User


class UserRepository:

    @staticmethod
    def get_by_email(db: Session, email: str):
        return db.exec(
            select(User).where(User.email == email)
        ).first()

    @staticmethod
    def create(db: Session, user: User):
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def get_by_id(db: Session, user_id: int):
        return db.get(User, user_id)
