from sqlalchemy import Column, Integer, DateTime, String, Date
from config.db import Base, engine
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
class Appointment(Base):
    __tablename__ = 'appointments'

    id = Column(Integer, primary_key=True, index=True)
    date_day = Column(Date)
    diagnosis = Column(String(255))
    treatment = Column(String(255))
    description = Column(String(255))
    petId = Column(Integer)
    veterinarian_id = Column(Integer, ForeignKey('veterinarians.id'), nullable=False)
    start_time = Column(String(8))  # Almacenar como cadena "HH:MM:SS"
    end_time = Column(String(8))    # Almacenar como cadena "HH:MM:SS"
    
    veterinarian = relationship('Veterinarian', back_populates='appointments')
