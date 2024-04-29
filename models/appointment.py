from sqlalchemy import Column, Integer, DateTime, String
from config.db import Base, engine

class Appointment(Base):
    __tablename__ = 'appointments'

    id = Column(Integer, primary_key=True, index=True)
    datetime = Column(String(255))
    diagnosis = Column(String(255))
    treatment = Column(String(255))
    description = Column(String(255))
    petId = Column(Integer)
    veterinarianId = Column(Integer)
    
