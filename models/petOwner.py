from sqlalchemy import Column, Integer, String, Enum
from config.db import Base, engine


class PetOwner(Base):
    __tablename__ = 'petowners'
    id = Column(Integer, primary_key=True, index=True)
    userId = Column(Integer)
    numberPhone = Column(String(10))
    subscriptionType = Column(Enum('Basic', 'Advanced', 'Pro', name='subscription_type'), default='Basic')
    

