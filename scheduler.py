from requests import Session
import schedule
import time
from config.db import get_db
from fastapi import APIRouter, Depends, HTTPException, status

from services.availability import AvailabilityService

def weekly_job(db: Session):
    print("Creando horarios de disponibilidad para la semana...")
    AvailabilityService.create_weekly_availabilities(db)  # Asegúrate de pasar tu sesión de base de datos db aquí

def weekly_cleanup(db: Session):
    print("Eliminando horarios de disponibilidad de la semana pasada...")
    AvailabilityService.delete_weekly_availabilities(db)  # Asegúrate de pasar tu sesión de base de datos db aquí

def run_job_once(db: Session):
    print("Ejecutando tarea semanal una única vez...")
    AvailabilityService.create_weekly_availabilities(db)
    schedule.cancel_job(run_job_once)  # Cancela la tarea después de ejecutarse una vez

# Ejecutar la tarea una sola vez ahora
db = next(get_db())
run_job_once(db)

# Programar la creación de horarios al comienzo de cada semana
schedule.every().sunday.at("23:59").do(weekly_job, db=db)

# Programar la limpieza de horarios al final de cada semana
schedule.every().sunday.at("23:59").do(weekly_cleanup, db=db)

# Ejecutar el planificador
while True:
    schedule.run_pending()
    time.sleep(1)
