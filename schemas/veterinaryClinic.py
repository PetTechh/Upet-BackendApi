from pydantic import BaseModel

from models.veterinaryClinic import VeterinaryClinic


class VeterinaryClinicSchemaPost(BaseModel):
    name: str
    location: str
    office_hours: str
    phone_number: str
    description: str
    
    def to_model(self) -> VeterinaryClinic:
        return VeterinaryClinic(
            name=self.name,
            location=self.location,
            office_hours=self.office_hours,
            phone_number=self.phone_number,
            description=self.description
        )
    
class VeterinaryClinicSchemaGet(BaseModel):
    id: int
    name: str
    location: str
    services: str
    office_hours: str
    image_url: str
    description: str

