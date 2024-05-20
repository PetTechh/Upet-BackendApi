from sqlalchemy import Boolean, Column, Integer, String, Enum
from config.db import Base, engine
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey

class Veterinarian(Base):
    __tablename__ = 'veterinarians'
    id = Column(Integer, primary_key=True, index=True)
    userId = Column(Integer, ForeignKey('users.id'))
    clinicId = Column(Integer)

    user = relationship("User", back_populates="veterinarian")
