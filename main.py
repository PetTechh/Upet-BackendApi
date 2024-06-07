from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import threading
import schedule
import time
from fastapi import Depends
from sqlalchemy.orm import Session
import uvicorn
from config.db import SessionLocal, get_db
from services.availability import AvailabilityService


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
from routes.review import reviews as review_router
from auth.routes.auth import auth as auth_router
from config.routes import prefix
Base.metadata.create_all(bind=engine)

app = FastAPI()


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

def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def check_and_reset_availabilities():
    db = next(get_db_session())
    try:
        print("Checking and resetting availabilities")
        AvailabilityService.delete_weekly_availabilities(db)
        AvailabilityService.create_weekly_availabilities(db)
    finally:
        db.close()
    schedule.clear()  # Detiene el planificador después de ejecutar la tarea

def schedule_check_and_reset():
    schedule.every().day.at("23:28").do(check_and_reset_availabilities)

def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

# Inicia la tarea de programación
schedule_check_and_reset()

# Inicia un hilo para ejecutar el ciclo de programación en segundo plano
threading.Thread(target=run_schedule, daemon=True).start()

if __name__ == "__main__":
    # Ejecuta la aplicación FastAPI en el puerto 8000
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info", reload=True)