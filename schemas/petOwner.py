from pydantic import BaseModel, Field
from Enums.subscriptionTypeEnum import SubscriptionType


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
    