from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from config.db import get_db
from models.appointment import Appointment
from models.user import Veterinarian
from models.pet import Pet
from schemas.appointment import AppointmentSchemaGet, AppointmentSchemaPost
from datetime import datetime

appointments = APIRouter()
tag = "appointments"

@appointments.get("/appointments/", response_model=list[AppointmentSchemaGet], status_code=status.HTTP_200_OK, tags=[tag])
def get_appointments(db: Session = Depends(get_db)):
    return db.query(Appointment).all()

@appointments.get("/appointments/pet/{pet_id}", response_model=list[AppointmentSchemaGet], status_code=status.HTTP_200_OK, tags=[tag])
def get_appointments_by_pet_id(pet_id: int, db: Session = Depends(get_db)):
    pet= db.query(Pet).filter(Pet.id == pet_id).first()
    if not pet:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="La mascota no existe.")
    appointments = db.query(Appointment).filter(Appointment.petId == pet_id).all()
    if not appointments:
        print("La mascota no tiene citas registradas.")
    return appointments

@appointments.get("/appointments/veterinarian/{veterinarian_id}", response_model=list[AppointmentSchemaGet], status_code=status.HTTP_200_OK, tags=[tag])
def get_appointments_by_veterinarian_id(veterinarian_id: int, db: Session = Depends(get_db)):
    veterinarian = db.query(Veterinarian).filter(Veterinarian.id == veterinarian_id).first()
    if not veterinarian:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El veterinario no existe.")
    
    
    appointments = db.query(Appointment).filter(Appointment.veterinarianId == veterinarian_id).all()
    
    if not appointments:
        print("El veterinario no tiene citas registradas.")
         
    return appointments


@appointments.post("/appointments/", response_model=AppointmentSchemaGet, status_code=status.HTTP_201_CREATED, tags=[tag])
def create_appointment(appointment: AppointmentSchemaPost, db: Session = Depends(get_db)):
    
    if not is_valid_datetime_format(appointment.datetime):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El formato de la fecha y hora debe ser 'YYYY-MM-DD HH:MM:SS'.")
    
    
    pet = db.query(Pet).filter(Pet.id == appointment.petId).first()
    if not pet:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="La mascota no existe.")
    
    
    veterinarian = db.query(Veterinarian).filter(Veterinarian.id == appointment.veterinarianId).first()

    if not veterinarian:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El veterinario no existe.")
    
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