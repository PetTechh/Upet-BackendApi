from pydantic import BaseModel, Field
from enum import Enum
from datetime import date
from Enums.speciesEnum import SpecieEnum
from Enums.genderEnum import GenderEnum


class PetSchemaPost(BaseModel):
    name: str
    breed: str
    species: SpecieEnum
    weight: float = Field(..., gt=0)  # Validar que weight sea mayor a 0
    birthdate: date  
    image_url: str
    gender: GenderEnum

class PetSchemaResponse(BaseModel):
    id: int
    name: str
    petOwnerId: int
    breed: str
    species: SpecieEnum
    weight: float
    birthdate: date  
    image_url: str
    gender: GenderEnum