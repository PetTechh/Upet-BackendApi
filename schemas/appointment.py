from pydantic import BaseModel, Field
from datetime import datetime

class AppointmentSchemaPost(BaseModel):
    datetime: str
    diagnosis: str
    treatment: str
    description: str

class AppointmentSchemaGet(BaseModel):
    id: int
    datetime: str
    diagnosis: str
    treatment: str
    description: str
