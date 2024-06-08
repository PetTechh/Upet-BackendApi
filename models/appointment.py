from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, String, Date, Time
from config.db import Base, engine
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
class Appointment(Base):
    __tablename__ = 'appointments'

    id = Column(Integer, primary_key=True, index=True)
    date_day = Column(Date, nullable=False, default=datetime.utcnow)
    diagnosis = Column(String(255), nullable=True)
    treatment = Column(String(255),  nullable=True)
    description = Column(String(255))
    pet_id = Column(Integer, ForeignKey('pets.id'), nullable=False)
    veterinarian_id = Column(Integer, ForeignKey('veterinarians.id'), nullable=False)
    start_time = Column(Time)  # Almacenar como cadena "HH:MM:SS"
    end_time = Column(Time)    # Almacenar como cadena "HH:MM:SS"
    
    pet = relationship('Pet', back_populates='appointments')
    veterinarian = relationship('Veterinarian', back_populates='appointments')
