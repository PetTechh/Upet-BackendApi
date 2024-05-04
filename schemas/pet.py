from pydantic import BaseModel, Field
from enum import Enum


class GenderEnum(str, Enum):
    Male = "Male",
    Female = "Female"


class PetSchemaPost(BaseModel):
    name: str
    breed: str
    species: str
    weight: float = Field(..., gt=0)  # Validar que weight sea mayor a 0
    age: int = Field(..., gt=0)  # Validar que age sea mayor a 0
    image_url: str
    gender: GenderEnum

class PetSchemaResponse(BaseModel):
    id: int
    name: str
    petOwnerId: int
    breed: str
    species: str
    weight: float
    age: int
    image_url: str
    gender: GenderEnum