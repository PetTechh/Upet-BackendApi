from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from config.db import get_db
from models.vaccination import Vaccination
from schemas.vaccination import VaccinationSchemaGet, VaccinationSchemaPost

vaccinations = APIRouter()
tag = "Vaccinations"
endpoint = "/vaccinations"

@vaccinations.get(endpoint, response_model=list[VaccinationSchemaGet], status_code=status.HTTP_200_OK, tags=[tag])
def get_vaccinations(db: Session = Depends(get_db)):
    return db.query(Vaccination).all()


@vaccinations.post(endpoint, response_model=VaccinationSchemaGet, status_code=status.HTTP_201_CREATED, tags=[tag])
def create_vaccination(vaccination: VaccinationSchemaPost, db: Session = Depends(get_db)):
    vaccinationName = db.query(Vaccination).filter(Vaccination.name == vaccination.name).first()
    if vaccinationName:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La vacuna ya existe.")
    
    new_vaccination = Vaccination(**vaccination.dict())
    db.add(new_vaccination)
    db.commit()
    return new_vaccination

