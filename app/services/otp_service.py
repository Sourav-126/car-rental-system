import random
from app.core.redis import redis_client


class OTPService:
    OTP_TTL_SECONDS = 300  

    @staticmethod
    def generate() -> str:
        return str(random.randint(100000, 999999))

    @staticmethod
    def save(key: str, otp: str):
        redis_client.setex(
            name=f"otp:{key}",
            time=OTPService.OTP_TTL_SECONDS,
            value=otp
        )

    @staticmethod
    def verify(key: str, otp: str) -> bool:
        stored_otp = redis_client.get(f"otp:{key}")

        if not stored_otp:
            return False

        if stored_otp != otp:
            return False

        redis_client.delete(f"otp:{key}")
        return True
