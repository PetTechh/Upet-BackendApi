from sqlalchemy import Boolean, Column, Integer, String, Enum
from config.db import Base, engine

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(155))
    email = Column(String(155), unique=True, index=True)
    password = Column(String(155))
    userType = Column(Enum('Vet', 'Owner', name='user_type'))
    registered = Column(Boolean, default=False)  
    

class PetOwner(Base):
    __tablename__ = 'petowners'
    id = Column(Integer, primary_key=True, index=True)
    userId = Column(Integer)
    subscriptionType = Column(Enum('Basic', 'Advanced', 'Pro', name='subscription_type'), default='Basic')
    
class Veterinarian(Base):
    __tablename__ = 'veterinarians'
    id = Column(Integer, primary_key=True, index=True)
    userId = Column(Integer)
    clinicId = Column(Integer)

Base.metadata.create_all(bind=engine)
