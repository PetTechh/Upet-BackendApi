from pydantic import BaseModel

class VeterinarianSchemaPost(BaseModel):
    clinicId :int
    
class VeterinarianSchemaGet(BaseModel):
    id: int
    userId: int
    clinicId :int

