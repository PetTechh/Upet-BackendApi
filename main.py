import os
import uvicorn
from config.db import SessionLocal
from models.availability import Availability
from scheduler import check_and_reset_availabilities
from apscheduler.triggers.cron import CronTrigger


from routes.user import users as user_router
from fastapi import FastAPI
from config.db import Base, engine
from routes.veterinaryClinic import veterinary_clinics as veterinary_clinic_router
from routes.pet import pets as pet_router
from routes.appointment import appointments as appointment_router
from routes.notification import notifications as notification_router
from routes.medicalHistory import medical_histories as medical_history_router
from routes.petOwner import pet_owners as pet_owner_router
from routes.veterinarian import veterinarians as veterinarian_router
from routes.disease import diseases as disease_router
from routes.vaccination import vaccinations as vaccine_router
from routes.review import reviews as review_router
from routes.availability import availabilities as availability_router
from auth.routes.auth import auth as auth_router
from config.routes import prefix
from apscheduler.schedulers.background import BackgroundScheduler
from contextlib import asynccontextmanager
from scheduler import check_and_reset_availabilities

Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = BackgroundScheduler()
    scheduler.start()
    
    def job_wrapper():
        db = SessionLocal()
        print("Running job")
        if db.query(Availability).count() == 0:
            check_and_reset_availabilities(db)
        db.close()

    scheduler.add_job(job_wrapper, trigger=CronTrigger(day_of_week="sun", hour=0, minute=0))
    yield
    scheduler.shutdown()

app = FastAPI(lifespan=lifespan)


app.include_router(auth_router,  prefix= prefix)
app.include_router(user_router, prefix= prefix)
app.include_router(veterinary_clinic_router,  prefix= prefix)
app.include_router(pet_router,  prefix= prefix)
app.include_router(appointment_router,  prefix= prefix)
app.include_router(notification_router,  prefix= prefix)
app.include_router(medical_history_router,  prefix= prefix)
app.include_router(pet_owner_router,  prefix= prefix)
app.include_router(veterinarian_router, prefix= prefix)
app.include_router(disease_router, prefix= prefix)
app.include_router(vaccine_router,  prefix= prefix)
app.include_router(review_router,  prefix= prefix)
app.include_router(availability_router,  prefix= prefix)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
