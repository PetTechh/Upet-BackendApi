from sqlalchemy import Boolean, Column, Integer, String, Enum
from config.db import Base
from Enums.userTypeEnum import UserType
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(155))
    email = Column(String(155), unique=True, index=True)
    password = Column(String(155))
    userType = Column(Enum(UserType, name='user_type'))
    registered = Column(Boolean, default=False)  
    image_url = Column(String(255), default="https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png")
