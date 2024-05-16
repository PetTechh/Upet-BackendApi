from fastapi import Depends, HTTPException, status
from config.db import get_db
from routes.user import endpoint as user_endpoint
from models.user import User
from models.petOwner import PetOwner
from schemas.petOwner import PetOwnerSchemaPost, SubscriptionType
from sqlalchemy.orm import Session
from auth.schemas.auth import UserType
from services.userService import UserService
from schemas.petOwner import PetOwnerSchemaGetByID

class PetOwnerService:
    @staticmethod
    def create_new_petowner(user_id: int, petowner: PetOwnerSchemaPost, db: Session = Depends(get_db)):
        user = UserService.get_user_by_id(user_id, db)

        # Verificar que el userType sea Owner
        if user.userType != UserType.Owner:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no es un propietario de mascotas.")

        if user.registered== True:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario ya ha sido registrado")

        if len(petowner.numberPhone) != 10:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El número de teléfono debe tener 10 dígitos.")

        new_petowner = PetOwner(userId=user_id, numberPhone= petowner.numberPhone , subscriptionType=SubscriptionType.Basic)
        db.add(new_petowner)
        user.registered = True
        db.commit()
        return new_petowner

    @staticmethod
    def get_petowners(db: Session = Depends(get_db)):
        return db.query(PetOwner).all()
    
    @staticmethod
    def get_petowner_by_user_id(user_id: int, db: Session):
        return db.query(PetOwner).filter(PetOwner.userId == user_id).first()    
    
    @staticmethod
    def get_petOwner_by_id(petOwner_id: int, db: Session) -> PetOwnerSchemaGetByID:
        
        petOwner = db.query(PetOwner).filter(PetOwner.id == petOwner_id).first()
        if not petOwner:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Veterinarian not found")
        
        user = db.query(User).filter(User.id == petOwner.userId).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        return PetOwnerSchemaGetByID(id=petOwner.id, userId=petOwner.userId, name=user.name, numberPhone=petOwner.numberPhone, subscriptionType=petOwner.subscriptionType)
    