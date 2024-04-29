from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from config.db import get_db
from models.disease import Disease
from schemas.disease import DiseaseSchemaGet, DiseaseSchemaPost

diseases = APIRouter()
tag = "Diseases"
endpoint = "/diseases"

@diseases.get(endpoint, response_model=list[DiseaseSchemaGet], status_code=status.HTTP_200_OK, tags=[tag])
def get_diseases(db: Session = Depends(get_db)):
    return db.query(Disease).all()

@diseases.post(endpoint, response_model=DiseaseSchemaGet, status_code=status.HTTP_201_CREATED, tags=[tag])
def create_disease(disease: DiseaseSchemaPost, db: Session = Depends(get_db)):
    diseaseName = db.query(Disease).filter(Disease.name == disease.name).first()
    if diseaseName:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La enfermedad ya existe.")

    new_disease = Disease(**disease.dict())
    db.add(new_disease)
    db.commit()
    return new_disease

