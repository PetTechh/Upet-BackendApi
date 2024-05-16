from fastapi import Depends, HTTPException, status
from config.db import get_db
from routes.user import endpoint as user_endpoint
from models.user import User
from models.petOwner import PetOwner
from schemas.petOwner import PetOwnerSchemaPost, SubscriptionType
from sqlalchemy.orm import Session
from auth.schemas.auth import UserType

class UserService:
    
    @staticmethod
    def get_user_by_id(user_id: int, db: Session):
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El usuario no existe o no es un propietario de mascotas no registrado.")
        return user