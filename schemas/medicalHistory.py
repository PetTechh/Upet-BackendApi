from pydantic import BaseModel

class MedicalHistorySchemaPost(BaseModel):
    petId: int
    date: str
    description: str
        
class MedicalHistorySchemaGet(BaseModel):
    id: int
    petId: int
    date: str
    description: str
