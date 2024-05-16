from sqlalchemy import Column, Integer, String, DECIMAL, ForeignKey, Enum, Date
from config.db import Base, engine
SpeciesEnum = Enum('Dog', 'Cat', name='species_enum')

class Pet(Base):
    __tablename__ = 'pets'
    id = Column(Integer, primary_key=True, index=True)
    name= Column(String(255))
    petOwnerId = Column(Integer, ForeignKey('petowners.id'))
    breed = Column(String(255))
    species = Column(Enum(SpeciesEnum))
    weight = Column(DECIMAL)
    birthdate = Column(Date)
    image_url = Column(String(255))
    gender = Column(Enum("Male","Female", name='gender'))
