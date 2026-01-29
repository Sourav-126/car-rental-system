from sqlmodel import Session, select
from app.models.vehicle import Vehicle


class VehicleRepository:

    @staticmethod
    def create(db: Session, vehicle: Vehicle):
        db.add(vehicle)
        db.commit()
        db.refresh(vehicle)
        return vehicle

    @staticmethod
    def list_active(db: Session):
        return db.exec(
            select(Vehicle).where(Vehicle.is_active == True)
        ).all()

    @staticmethod
    def get(db: Session, vehicle_id: int):
        return db.get(Vehicle, vehicle_id)

    @staticmethod
    def delete(db: Session, vehicle: Vehicle):
        db.delete(vehicle)
        db.commit()

    @staticmethod
    def list_all(db: Session):
        return db.exec(select(Vehicle)).all()