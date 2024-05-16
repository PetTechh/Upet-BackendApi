from pydantic import BaseModel
from Enums.userTypeEnum import UserType



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


