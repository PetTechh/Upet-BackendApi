from sqlalchemy import Column, Integer, String
from config.db import Base

class Vaccination(Base):
    __tablename__ = 'vaccinations'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
