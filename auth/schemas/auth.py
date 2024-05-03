from pydantic import BaseModel
from enum import Enum

class CreateUserRequest (BaseModel):
    email: str
    password: str

class Token (BaseModel):
    access_token: str
    token_type: str


class UserType(str, Enum):
    Vet = "Vet"
    Owner = "Owner"

class UserSchemaPost(BaseModel):
    name: str
    email: str
    password: str
    userType: UserType

