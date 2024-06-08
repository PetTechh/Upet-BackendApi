import random
import string
import datetime
from sqlalchemy.orm import Session
from models.otps import OTP
from config.db import get_db
from fastapi import HTTPException, status, Depends
from models.appointment import Appointment
from models.pet import Pet
from models.veterinarian import Veterinarian
from schemas.appointment import AppointmentSchemaGet, AppointmentSchemaPost

class AppointmentService:

    @staticmethod
    def get_all_appointments(db: Session):
        appointments = db.query(Appointment).all()
        for appointment in appointments:
            appointments = AppointmentSchemaGet.from_orm(appointment)
        return appointments

    @staticmethod
    def get_appointments_by_pet_id(pet_id: int, db: Session):
        pet = db.query(Pet).filter(Pet.id == pet_id).first()
        if not pet:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="La mascota no existe.")
        appointments = db.query(Appointment).filter(Appointment.pet_id == pet_id).all()
        if not appointments:
            print("La mascota no tiene citas registradas.")
        return appointments

    @staticmethod
    def get_appointments_by_veterinarian_id(veterinarian_id: int, db: Session):
        veterinarian = db.query(Veterinarian).filter(Veterinarian.id == veterinarian_id).first()
        if not veterinarian:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El veterinario no existe.")
        appointments = db.query(Appointment).filter(Appointment.veterinarian_id == veterinarian_id).all()
        if not appointments:
            print("El veterinario no tiene citas registradas.")
        return appointments

    @staticmethod
    def create_appointment(appointment: AppointmentSchemaPost, db: Session):

        pet = db.query(Pet).filter(Pet.id == appointment.pet_id).first()
        if not pet:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="La mascota no existe.")
        
        veterinarian = db.query(Veterinarian).filter(Veterinarian.id == appointment.veterinarian_id).first()
        if not veterinarian:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El veterinario no existe.")
        
        new_appointment = appointment.to_model()
        db.add(new_appointment)
        db.commit()
        db.refresh(new_appointment)
        return new_appointment
