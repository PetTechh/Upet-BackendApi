from pydantic import BaseModel

class VeterinaryClinicSchemaPost(BaseModel):
    name: str
    location: str
    office_hours: str
    phone_number: str
    
class VeterinaryClinicSchemaGet(BaseModel):
    id: int
    name: str
    location: str
    services: str
    office_hours: str
    image_url: str
