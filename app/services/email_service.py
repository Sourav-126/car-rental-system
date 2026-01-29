import smtplib
from email.message import EmailMessage
from app.core.config import settings


class EmailService:

    @staticmethod
    def send_otp(to_email: str, otp: str):
        msg = EmailMessage()
        msg["Subject"] = "Your KYC Verification OTP"
        msg["From"] = settings.EMAIL_FROM
        msg["To"] = to_email

        msg.set_content(
            f"""
Your OTP for KYC verification is:

{otp}

This OTP is valid for 5 minutes.
Do not share it with anyone.
"""
        )

        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
            server.send_message(msg)
