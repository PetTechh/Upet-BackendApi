from pydantic import BaseModel

class VeterinaryClinicSchemaPost(BaseModel):
    name: str
    location: str
    services: str
    hours:str

class VeterinaryClinicSchemaGet(BaseModel):
    id: int
    name: str
    location: str
    services: str
    hours:str