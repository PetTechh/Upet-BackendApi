from sqlalchemy import Column, Date, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from config.db import Base, engine

class Notification(Base):
    __tablename__ = 'notifications'

    id = Column(Integer, primary_key=True, index=True)
    petOwnerId = Column(Integer, ForeignKey('petowners.id'))
    type = Column(String(255))
    message = Column(String(255))
    datetime = Column(DateTime)


