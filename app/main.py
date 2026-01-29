from fastapi import FastAPI
from app.routers import auth, booking, kyc, vehicle, admin, user

app = FastAPI(title="Car Rental System")

app.include_router(auth.router)
app.include_router(booking.router)
app.include_router(kyc.router)
app.include_router(vehicle.router)
app.include_router(admin.router)
app.include_router(user.router)
