from datetime import date
from pydantic import BaseModel


class NotificationSchemaPost(BaseModel):
    petOwnerId: int
    type: str
    message: str
    datetime: date

class NotificationSchemaGet(BaseModel):
    id: int
    petOwnerId: int
    type: str
    message: str
    datetime: date