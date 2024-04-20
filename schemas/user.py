from pydantic import BaseModel, Field
from enum import Enum

class UserType(str, Enum):
    Vet = "Vet"
    Owner = "Owner"

class SubscriptionType(str, Enum):
    Basic = "Basic"
    Advanced = "Advanced"
    Pro = "Pro"

class UserSchemaGet(BaseModel):
    id: int
    name: str
    email: str
    password: str
    userType: UserType
    registered: bool  # Agregar el campo registrado


class UserSchemaPost(BaseModel):
    name: str
    email: str
    password: str
    userType: UserType


class PetOwnerSchemaPost(BaseModel):
    numberPhone: str

class PetOwnerSchemaGet(BaseModel):
    id: int
    userId: int
    numberPhone: str
    subscriptionType: SubscriptionType
    
class VeterinarianSchemaPost(BaseModel):
    clinicId :int
    
class VeterinarianSchemaGet(BaseModel):
    id: int
    userId: int
    clinicId :int