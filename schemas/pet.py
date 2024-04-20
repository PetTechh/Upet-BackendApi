from pydantic import BaseModel, Field

class PetSchemaPost(BaseModel):
    name: str
    breed: str
    species: str
    weight: float = Field(..., gt=0)  # Validar que weight sea mayor a 0
    age: int = Field(..., gt=0)  # Validar que age sea mayor a 0

class PetSchemaGet(BaseModel):
    id: int
    name: str
    petOwnerId: int
    breed: str
    species: str
    weight: float
    age: int