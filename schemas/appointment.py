from pydantic import BaseModel, Field

class AppointmentSchemaPost(BaseModel):
    datetime: str
    diagnosis: str
    treatment: str
    description: str
    petId: int
    veterinarianId: int

class AppointmentSchemaGet(BaseModel):
    id: int
    datetime: str
    diagnosis: str
    treatment: str
    description: str
    petId: int
    veterinarianId: int
