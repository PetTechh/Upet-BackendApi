from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from config.db import get_db

from models.medicalHistory import MedicalHistory
from models.medicalHistoryRelationships import MedicalHistoryDisease, MedicalHistoryVaccination
from models.disease import Disease
from models.vaccination import Vaccination

from schemas.medicalHistory import  MedicalHistorySchemaPost, MedicalHistorySchemaGet
from schemas.medicalHistoryRelationships import MedicalHistoryVaccinationSchemaGet, MedicalHistoryVaccinationSchemaPost
from schemas.medicalHistory import MedicalHistorySchemaGet
from schemas.medicalHistoryRelationships import MedicalHistoryDiseaseSchemaGet, MedicalHistoryDiseaseSchemaPost



from models.pet import Pet


medical_historys = APIRouter()
tag = "Medical Historys"
endpoint = "/medical_historys"


#Get All medical historys
@medical_historys.get(endpoint, response_model=list[MedicalHistorySchemaGet], status_code=status.HTTP_200_OK, tags=[tag])
def get_medical_history(db: Session = Depends(get_db)):
    return db.query(MedicalHistory).all()


#Get All diseases by medical history
@medical_historys.get(endpoint + "/{medical_history_id}/diseases/", response_model=list[MedicalHistoryDiseaseSchemaGet], status_code=status.HTTP_200_OK, tags=[tag])
def get_medical_history_diseases(medical_history_id: int, db: Session = Depends(get_db)):
    
    medical_history_diseases = db.query(MedicalHistoryDisease).filter(MedicalHistoryDisease.historyId == medical_history_id).all()
    
    if medical_history_diseases == []:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El historial médico no tiene enfermedades registradas.")

    return medical_history_diseases


# Create a new medical history
@medical_historys.post(endpoint, response_model=MedicalHistorySchemaGet, status_code=status.HTTP_201_CREATED, tags=[tag])
def create_medical_history(medical_history: MedicalHistorySchemaPost, db: Session = Depends(get_db)):
    
    pet = db.query(Pet).filter(Pet.id == medical_history.petId).first()
    if not pet:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="La mascota no existe.")
    
    medical_history_router= db.query(MedicalHistory).filter(MedicalHistory.petId == medical_history.petId).first()
    if medical_history_router:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La mascota ya tiene un historial médico.")
    
    new_medical_history = MedicalHistory(**medical_history.dict())
    db.add(new_medical_history)
    db.commit()
    return new_medical_history


# Add a disease to an existing medical history
@medical_historys.post(endpoint + "/{medicalHistory_id}", response_model=MedicalHistoryDiseaseSchemaGet, status_code=status.HTTP_201_CREATED, tags=[tag])
def create_medical_history_disease(medicalHistory_id: int, medical_history_disease: MedicalHistoryDiseaseSchemaPost, db: Session = Depends(get_db)):
    medicalHistory = db.query(MedicalHistory).filter(MedicalHistory.id == medicalHistory_id).first()
    if not medicalHistory:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El historial médico no existe.")
    
    new_medical_history_disease = MedicalHistoryDisease(historyId=medicalHistory_id, **medical_history_disease.dict())
  
    if db.query(Disease).filter(Disease.id == new_medical_history_disease.diseaseId).first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="La enfermedad no existe.")
    
    if db.query(MedicalHistoryDisease).filter(MedicalHistoryDisease.historyId == medicalHistory_id, MedicalHistoryDisease.diseaseId == new_medical_history_disease.diseaseId).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La enfermedad ya está registrada en el historial médico.")
  
    db.add(new_medical_history_disease)
    db.commit()
    return new_medical_history_disease


# Add a vaccination to an existing medical history
@medical_historys.post(endpoint+ "/{medicalHistory_id}", response_model=MedicalHistoryVaccinationSchemaGet, status_code=status.HTTP_201_CREATED, tags=[tag])
def create_medical_history_vaccination(medicalHistory_id: int, medical_history_vaccination: MedicalHistoryVaccinationSchemaPost, db: Session = Depends(get_db)):
    medicalHistory = db.query(MedicalHistory).filter(MedicalHistory.id == medicalHistory_id).first()
    if not medicalHistory:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El historial médico no existe.")
    
    new_medical_history_vaccination = MedicalHistoryVaccination(historyId=medicalHistory_id, **medical_history_vaccination.dict())
  
    if db.query(Vaccination).filter(Vaccination.id == new_medical_history_vaccination.vaccinationId).first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="La vacuna no existe.")
    
    vaccination_record = db.query(MedicalHistoryVaccination).filter(MedicalHistoryVaccination.historyId == medicalHistory_id, MedicalHistoryVaccination.vaccinationId == new_medical_history_vaccination.vaccinationId).first()
    if vaccination_record:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La vacuna ya está registrada en el historial médico.")

    if medical_history_vaccination.dose < 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La dosis debe ser mayor a 0.")

    db.add(new_medical_history_vaccination)
    db.commit()
    return new_medical_history_vaccination


# Get All vaccinations by medical history
@medical_historys.get(endpoint + "/{medical_history_id}/vaccinations/", response_model=list[MedicalHistoryVaccinationSchemaGet], status_code=status.HTTP_200_OK, tags=[tag])
def get_medical_history_vaccinations(medical_history_id: int, db: Session = Depends(get_db)):
    
    medical_history_vaccinations = db.query(MedicalHistoryVaccination).filter(MedicalHistoryVaccination.historyId == medical_history_id).all()
    
    if medical_history_vaccinations == []:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El historial médico no tiene vacunas registradas.")

    return medical_history_vaccinations

# Update vaccination information in a medical history
@medical_historys.put(endpoint + "/{medicalHistoryId}", response_model=MedicalHistoryVaccinationSchemaGet, status_code=status.HTTP_200_OK, tags=[tag])
def update_medical_history_vaccination(medicalHistoryId: int, medical_history_vaccination: MedicalHistoryVaccinationSchemaPost, db: Session = Depends(get_db)):
    vaccination_record = db.query(MedicalHistoryVaccination).filter(
        MedicalHistoryVaccination.historyId == medicalHistoryId,
        MedicalHistoryVaccination.vaccinationId == medical_history_vaccination.vaccinationId
    ).first()
    
    if not vaccination_record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="La vacunación no existe.")
    
    if medical_history_vaccination.dose < 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La dosis debe ser mayor a 0.")
    
    if vaccination_record.dose != medical_history_vaccination.dose - 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La dosis debe ser consecutiva.")
    
    vaccination_record.dose = medical_history_vaccination.dose
    db.commit()
    return vaccination_record
