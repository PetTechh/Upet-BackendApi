from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from config.db import get_db
from models.medicalHistory import Disease, MedicalHistory, MedicalHistoryDisease, Vaccination, MedicalHistoryVaccination
from schemas.medicalHistory import DiseaseSchemaGet, DiseaseSchemaPost , MedicalHistorySchemaPost, MedicalHistorySchemaGet, MedicalHistoryVaccinationSchemaGet, MedicalHistoryVaccinationSchemaPost
from schemas.medicalHistory import MedicalHistorySchemaGet, MedicalHistoryDiseaseSchemaGet, MedicalHistoryDiseaseSchemaPost, VaccinationSchemaGet, VaccinationSchemaPost
from models.pet import Pet
medical_history_router = APIRouter()
tag = "medical_history"

@medical_history_router.get("/diseases/", response_model=list[DiseaseSchemaGet], status_code=status.HTTP_200_OK, tags=[tag])
def get_diseases(db: Session = Depends(get_db)):
    return db.query(Disease).all()


@medical_history_router.post("/diseases/", response_model=DiseaseSchemaGet, status_code=status.HTTP_201_CREATED, tags=[tag])
def create_disease(disease: DiseaseSchemaPost, db: Session = Depends(get_db)):
    diseaseName = db.query(Disease).filter(Disease.name == disease.name).first()
    if diseaseName:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La enfermedad ya existe.")

    new_disease = Disease(**disease.dict())
    db.add(new_disease)
    db.commit()
    return new_disease



@medical_history_router.get("/medical_history/", response_model=list[MedicalHistorySchemaGet], status_code=status.HTTP_200_OK, tags=[tag])
def get_medical_history(db: Session = Depends(get_db)):
    return db.query(MedicalHistory).all()

@medical_history_router.get("/medical_history/{medical_history_id}/diseases/", response_model=list[MedicalHistoryDiseaseSchemaGet], status_code=status.HTTP_200_OK, tags=[tag])
def get_medical_history_diseases(medical_history_id: int, db: Session = Depends(get_db)):
    
    medical_history_diseases = db.query(MedicalHistoryDisease).filter(MedicalHistoryDisease.historyId == medical_history_id).all()
    
    if medical_history_diseases == []:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El historial médico no tiene enfermedades registradas.")

    return medical_history_diseases





@medical_history_router.post("/medical_history/", response_model=MedicalHistorySchemaGet, status_code=status.HTTP_201_CREATED, tags=[tag])
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


@medical_history_router.post("/medical_history_diseases/{medicalHistory_id}", response_model=MedicalHistoryDiseaseSchemaGet, status_code=status.HTTP_201_CREATED, tags=[tag])
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






@medical_history_router.get("/vaccinations/", response_model=list[VaccinationSchemaGet], status_code=status.HTTP_200_OK, tags=[tag])
def get_vaccinations(db: Session = Depends(get_db)):
    return db.query(Vaccination).all()


@medical_history_router.post("/vaccinations/", response_model=VaccinationSchemaGet, status_code=status.HTTP_201_CREATED, tags=[tag])
def create_vaccination(vaccination: VaccinationSchemaPost, db: Session = Depends(get_db)):
    vaccinationName = db.query(Vaccination).filter(Vaccination.name == vaccination.name).first()
    if vaccinationName:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La vacuna ya existe.")
    
    new_vaccination = Vaccination(**vaccination.dict())
    db.add(new_vaccination)
    db.commit()
    return new_vaccination





@medical_history_router.post("/medical_history_vaccinations/{medicalHistory_id}", response_model=MedicalHistoryVaccinationSchemaGet, status_code=status.HTTP_201_CREATED, tags=[tag])
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

@medical_history_router.get("/medical_history/{medical_history_id}/vaccinations/", response_model=list[MedicalHistoryVaccinationSchemaGet], status_code=status.HTTP_200_OK, tags=[tag])
def get_medical_history_vaccinations(medical_history_id: int, db: Session = Depends(get_db)):
    
    medical_history_vaccinations = db.query(MedicalHistoryVaccination).filter(MedicalHistoryVaccination.historyId == medical_history_id).all()
    
    if medical_history_vaccinations == []:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El historial médico no tiene vacunas registradas.")

    return medical_history_vaccinations


@medical_history_router.put("/medical_history_vaccinations/{medicalHistoryId}", response_model=MedicalHistoryVaccinationSchemaGet, status_code=status.HTTP_200_OK, tags=[tag])
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
