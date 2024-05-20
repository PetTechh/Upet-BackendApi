from pydantic import BaseModel
from models.veterinarian import Veterinarian
from models.user import User

class VeterinarianSchemaPost(BaseModel):
    clinicName: str
    otp_password: str
    

    
class VeterinarianSchemaGet(BaseModel):
    id: int
    name: str
    clinicId :int
    image_url: str
    userId: int
    
    class Config:
        orm_mode = True

    @classmethod
    def from_orm(cls, veterinarian: Veterinarian, user: User):
        return cls(
            id=veterinarian.id,
            name=user.name,
            image_url= user.image_url,
            userId=veterinarian.userId,
            clinicId=veterinarian.clinicId
        )