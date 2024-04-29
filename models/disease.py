from sqlalchemy import Column, Integer, String
from config.db import Base

class Disease(Base):
    __tablename__ = 'diseases'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))