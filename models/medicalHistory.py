from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from config.db import Base, engine

class Disease(Base):
    __tablename__ = 'diseases'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))


class Vaccination(Base):
    __tablename__ = 'vaccinations'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))

class MedicalHistory(Base):
    __tablename__ = 'medicalhistory'

    id = Column(Integer, primary_key=True, index=True)
    petId = Column(Integer, ForeignKey('pets.id'))
    date = Column(String(255))
    description = Column(String(255))

class MedicalHistoryDisease(Base):
    __tablename__ = 'medicalhistory_diseases'

    historyId = Column(Integer, ForeignKey('medicalhistory.id'), primary_key=True)
    diseaseId = Column(Integer, ForeignKey('diseases.id'), primary_key=True)
    date = Column(String(255))

class MedicalHistoryVaccination(Base):
    __tablename__ = 'medicalhistory_vaccinations'

    historyId = Column(Integer, ForeignKey('medicalhistory.id'), primary_key=True)
    vaccinationId = Column(Integer, ForeignKey('vaccinations.id'), primary_key=True)
    date = Column(String(255))
    dose = Column(Integer)
    vaccinationPlace = Column(String(255))
    
Base.metadata.create_all(bind=engine)
