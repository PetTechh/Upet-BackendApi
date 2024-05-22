from pydantic import BaseModel, Field
from Enums.subscriptionTypeEnum import SubscriptionType
from models.petOwner import PetOwner
from models.user import User

class PetOwnerSchemaPost(BaseModel):
    numberPhone: str
    location: str


class PetOwnerSchemaGet(BaseModel):
    id: int
    name: str
    numberPhone: str
    image_url: str
    location: str
    subscriptionType: SubscriptionType
    
    class Config:
        orm_mode = True

    @classmethod
    def from_orm(cls, petOwner: PetOwner, user: User):
        return cls(
            id=petOwner.id,
            name=user.name,
            numberPhone=petOwner.numberPhone,
            location=petOwner.location,
            image_url=user.image_url,
            subscriptionType=petOwner.subscriptionType
        )