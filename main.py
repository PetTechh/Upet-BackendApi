from fastapi import FastAPI
from routes.user import users as user_router
from routes.veterinaryClinic import veterinary_clinics as veterinary_clinic_router
from routes.pet import pets as pet_router
from routes.appointment import appointments as appointment_router
from routes.notification import notifications as notification_router

app = FastAPI()
app.include_router(user_router, prefix="/api")
app.include_router(veterinary_clinic_router, prefix="/api")
app.include_router(pet_router, prefix="/api")
app.include_router(appointment_router, prefix="/api")
app.include_router(notification_router, prefix="/api")