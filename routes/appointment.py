from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from config.db import get_db
from models.appointment import Appointment
from schemas.appointment import AppointmentSchemaGet, AppointmentSchemaPost
from datetime import datetime

appointments = APIRouter()
tag = "appointments"

@appointments.get("/appointments/", response_model=list[AppointmentSchemaGet], status_code=status.HTTP_200_OK, tags=[tag])
def get_appointments(db: Session = Depends(get_db)):
    return db.query(Appointment).all()

@appointments.post("/appointments/", response_model=AppointmentSchemaGet, status_code=status.HTTP_201_CREATED, tags=[tag])
def create_appointment(appointment: AppointmentSchemaPost, db: Session = Depends(get_db)):
    
    if not is_valid_datetime_format(appointment.datetime):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El formato de la fecha y hora debe ser 'YYYY-MM-DD HH:MM:SS'.")
    new_appointment = Appointment(**appointment.dict())
    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)
    return new_appointment


def is_valid_datetime_format(datetime_str: str) -> bool:
    try:
        datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
        return True
    except ValueError:
        return False