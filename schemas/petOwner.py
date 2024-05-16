from pydantic import BaseModel, Field
from enum import Enum

class SubscriptionType(str, Enum):
    Basic = "Basic"
    Advanced = "Advanced"
    Pro = "Pro"

class PetOwnerSchemaPost(BaseModel):
    numberPhone: str

class PetOwnerSchemaGet(BaseModel):
    id: int
    userId: int
    numberPhone: str
    subscriptionType: SubscriptionType

class PetOwnerSchemaGetByID(BaseModel):
    id: int
    name: str
    numberPhone: str
    subscriptionType: SubscriptionType
    