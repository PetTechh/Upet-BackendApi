from pydantic import BaseModel

class MedicalHistoryDiseaseSchemaGet(BaseModel):
    historyId: int
    diseaseId: int
    date: str

class MedicalHistoryDiseaseSchemaPost(BaseModel):
    diseaseId: int
    date: str

class MedicalHistoryVaccinationSchemaPost(BaseModel):
    vaccinationId: int
    date: str
    dose: int
    vaccinationPlace: str

class MedicalHistoryVaccinationSchemaGet(BaseModel):
    historyId: int
    vaccinationId: int
    date: str
    dose: int
    vaccinationPlace: str
