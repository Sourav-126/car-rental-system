from datetime import datetime

from app.models.kyc import KYC
from app.repositories.kyc_repository import KYCRepository
from app.services.otp_service import OTPService
from app.services.email_service import EmailService


class KYCService:

    @staticmethod
    def submit(db, user, payload):
        """
        Create KYC request + send OTP to email
        """

       
        kyc = KYC(
            user_id=user.id,
            document_type=payload.document_type,
            document_number=payload.document_number,
            email=payload.email,
            phone_number=payload.phone_number,
            status="PENDING",
        )

      
        otp = OTPService.generate()

        OTPService.save(payload.email, otp)

        EmailService.send_otp(
            to_email=payload.email,
            otp=otp
        )

        return KYCRepository.create(db, kyc)

    @staticmethod
    def verify(db, user, email: str, otp: str):
        """
        Verify OTP and approve KYC
        """

        if not OTPService.verify(email, otp):
            raise ValueError("Invalid or expired OTP")

        kyc = KYCRepository.get_by_email(db, email)

        if not kyc:
            raise ValueError("KYC record not found")

        kyc.status = "APPROVED"
        kyc.verified_at = datetime.utcnow()

        user.is_verified = True

        db.add(kyc)
        db.add(user)
        db.commit()
        db.refresh(kyc)

        return kyc