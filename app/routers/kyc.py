from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.schemas.kyc import KYCSubmitSchema, KYCVerifyOTPSchema
from app.services.kyc_service import KYCService
from app.core.database import get_db
from app.api.deps import get_current_user

router = APIRouter(tags=["KYC"], prefix="/kyc")

@router.post("/submit")
def submit(payload: KYCSubmitSchema,
           db: Session = Depends(get_db),
           user=Depends(get_current_user)):
    if payload.email != user.email:
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail="Email in KYC must match your account email")
    return KYCService.submit(db, user, payload)


@router.post("/verify")
def verify(payload: KYCVerifyOTPSchema,
           db: Session = Depends(get_db),
           user=Depends(get_current_user)):
    return KYCService.verify(db, user, payload.email, payload.otp)
