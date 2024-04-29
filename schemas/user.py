from pydantic import BaseModel
from enum import Enum

class UserType(str, Enum):
    Vet = "Vet"
    Owner = "Owner"

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


