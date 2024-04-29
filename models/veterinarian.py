from sqlalchemy import Boolean, Column, Integer, String, Enum
from config.db import Base, engine


class Veterinarian(Base):
    __tablename__ = 'veterinarians'
    id = Column(Integer, primary_key=True, index=True)
    userId = Column(Integer)
    clinicId = Column(Integer)

