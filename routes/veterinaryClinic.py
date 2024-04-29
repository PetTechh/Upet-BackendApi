from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from config.db import get_db

from schemas.veterinaryClinic import VeterinaryClinicSchemaGet, VeterinaryClinicSchemaPost
from models.veterinaryClinic import VeterinaryClinic

veterinary_clinics = APIRouter()
tag = "Veterinary Clinics"
endpoint = "/veterinary_clinics"

@veterinary_clinics.post(endpoint, response_model=VeterinaryClinicSchemaGet, status_code=status.HTTP_201_CREATED, tags=[tag])
def create_veterinary_clinic(clinic: VeterinaryClinicSchemaPost, db: Session = Depends(get_db)):
    new_clinic = {"name": clinic.name, 
                  "location": clinic.location, 
                  "services": clinic.services, 
                  "hours": clinic.hours}
    new_clinic = VeterinaryClinic(**new_clinic)
    db.add(new_clinic)
    db.commit()
    return new_clinic

@veterinary_clinics.get(endpoint, response_model=list[VeterinaryClinicSchemaGet], status_code=status.HTTP_200_OK, tags=[tag])
def get_veterinary_clinics(db: Session = Depends(get_db)):
    return db.query(VeterinaryClinic).all()
