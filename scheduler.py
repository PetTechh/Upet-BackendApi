from datetime import datetime
import schedule
import time
from fastapi import Depends
from sqlalchemy.orm import Session
from config.db import get_db
from services.availability import AvailabilityService

def check_and_reset_availabilities(db: Session = Depends(get_db)):
    AvailabilityService.delete_weekly_availabilities(db)
    AvailabilityService.create_weekly_availabilities(db)      
    schedule.clear()  # Detiene el planificador después de ejecutar la tarea
  
