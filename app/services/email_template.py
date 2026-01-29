def kyc_otp_email(otp: str) -> str:
    return f"""
Your KYC verification OTP is:

{otp}

This OTP is valid for 5 minutes.
Do not share this code with anyone.

– Car Rental System
"""
