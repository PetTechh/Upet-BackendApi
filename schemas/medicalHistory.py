from pydantic import BaseModel


class DiseaseSchemaPost(BaseModel):
    name: str

class DiseaseSchemaGet(BaseModel):
    id: int
    name: str


class VaccinationSchemaPost(BaseModel):
    name: str

class VaccinationSchemaGet(BaseModel):
    id: int
    name: str
    
    
class MedicalHistorySchemaPost(BaseModel):
    petId: int
    date: str
    description: str

        
class MedicalHistorySchemaGet(BaseModel):
    id: int
    petId: int
    date: str
    description: str



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
