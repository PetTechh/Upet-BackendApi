from sqlalchemy import Boolean, Column, Integer, String, Enum
from config.db import Base, engine

class VeterinaryClinic(Base):
    __tablename__ = 'veterinaryclinics'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    location = Column(String(255))
    services = Column(String(255))
    hours = Column(String(255))


Base.metadata.create_all(bind=engine)
