from app.repositories.user_repository import UserRepository
from app.core.security import verify_password, create_access_token, hash_password
from app.models.user import User


class AuthService:

    @staticmethod
    def register(db, payload):
        existing = UserRepository.get_by_email(db, payload.email)
        if existing:
            raise ValueError("Email already registered")
            
        hashed = hash_password(payload.password)
        user = User(
            email=payload.email,
            name=payload.name,
            hashed_password=hashed,
            role="USER"
        )
        return UserRepository.create(db, user)

    @staticmethod
    def login(db, email, password):
        user = UserRepository.get_by_email(db, email)
        if not user or not verify_password(password, user.hashed_password):
            raise ValueError("Invalid credentials")

        return create_access_token({"sub": str(user.id)})
