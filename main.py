from routes.user import users as user_router
from fastapi import FastAPI
from config.db import Base, engine
from routes.veterinaryClinic import veterinary_clinics as veterinary_clinic_router
from routes.pet import pets as pet_router
from routes.appointment import appointments as appointment_router
from routes.notification import notifications as notification_router
from routes.medicalHistory import medical_historys as medical_history_router
from routes.petOwner import pet_owners as pet_owner_router
from routes.veterinarian import veterinarians as veterinarian_router
from routes.disease import diseases as disease_router
from routes.vaccination import vaccinations as vaccine_router


Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(user_router, prefix="/api")
app.include_router(veterinary_clinic_router, prefix="/api")
app.include_router(pet_router, prefix="/api")
app.include_router(appointment_router, prefix="/api")
app.include_router(notification_router, prefix="/api")
app.include_router(medical_history_router, prefix="/api")
app.include_router(pet_owner_router, prefix="/api")
app.include_router(veterinarian_router, prefix="/api")
app.include_router(disease_router, prefix="/api")
app.include_router(vaccine_router, prefix="/api")

