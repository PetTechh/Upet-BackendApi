from sqlalchemy import Column, Integer, String, Enum
from config.db import Base, engine
from Enums.subscriptionTypeEnum import SubscriptionType

class PetOwner(Base):
    __tablename__ = 'petowners'
    id = Column(Integer, primary_key=True, index=True)
    userId = Column(Integer)
    numberPhone = Column(String(10))
    subscriptionType = Column(Enum(SubscriptionType, name='subscription_type'), default=SubscriptionType.Basic)
    

