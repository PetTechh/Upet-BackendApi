from sqlalchemy import Column, Integer, String, ForeignKey
from config.db import Base

class MedicalHistory(Base):
    __tablename__ = 'medicalhistory'

    id = Column(Integer, primary_key=True, index=True)
    petId = Column(Integer, ForeignKey('pets.id'))
    date = Column(String(255))
    description = Column(String(255))
