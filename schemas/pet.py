from pydantic import BaseModel, Field
from enum import Enum
from datetime import date


class GenderEnum(str, Enum):
    Male = "Male",
    Female = "Female"

class SpecieEnum(str, Enum):
    Dog = "Dog",
    Cat = "Cat",
    Bird = "Bird",
    Fish = "Fish",
    Reptile = "Reptile",
    Rodent = "Rodent",
    Rabbit = "Rabbit",
    Other = "Other"

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