from sqlalchemy import Column, Integer, String, Enum
from config.db import Base
from Enums.subscriptionTypeEnum import SubscriptionType
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from models.user import User  # Importa la clase User desde models.user

class PetOwner(Base):
    __tablename__ = 'petowners'
    id = Column(Integer, primary_key=True, index=True)
    userId = Column(Integer, ForeignKey('users.id'))
    numberPhone = Column(String(10))
    location = Column(String(50))
    subscriptionType = Column(Enum(SubscriptionType, name='subscription_type'), default=SubscriptionType.Basic)

    user = relationship("User", back_populates="pet_owner") 
    pets = relationship("Pet", back_populates="pet_owner", cascade="all, delete-orphan")    
    reviews = relationship('Review', back_populates='petowner')  # Relación con Review

from models.pet import Pet  # Importa la clase Pet después de la definición de PetOwner

