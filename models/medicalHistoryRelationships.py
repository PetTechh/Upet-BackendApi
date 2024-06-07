from sqlalchemy import Column, Integer, String, ForeignKey
from config.db import Base

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
