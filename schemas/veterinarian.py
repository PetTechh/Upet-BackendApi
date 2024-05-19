from pydantic import BaseModel

class VeterinarianSchemaPost(BaseModel):
    clinicName: str
    otp_password: str
    
class VeterinarianSchemaGet(BaseModel):
    id: int
    userId: int
    clinicId :int

class VeterinarianSchemaGetByID(BaseModel):
    id: int
    name: str
    clinicId :int
    image_url: str
