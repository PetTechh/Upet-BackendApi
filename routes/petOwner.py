from fastapi import APIRouter, Depends, HTTPException, status
from config.db import get_db

from routes.user import endpoint as user_endpoint

from models.user import User
from models.petOwner import PetOwner

from schemas.petOwner import PetOwnerSchemaGet, PetOwnerSchemaPost, SubscriptionType

from sqlalchemy.orm import Session

pet_owners = APIRouter()
tag = "Pet Owners"
endpoint = user_endpoint + "/petowner"

@pet_owners.post(endpoint +"/{user_id}", response_model=PetOwnerSchemaGet, status_code=status.HTTP_201_CREATED, tags=[tag])
def create_petowner(user_id: int, petowner: PetOwnerSchemaPost, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El usuario no existe o no es un propietario de mascotas no registrado.")
    
    # Verificar que el userType sea Owner
    if user.userType != "Owner":
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

@pet_owners.get(endpoint, response_model=list[PetOwnerSchemaGet], status_code=status.HTTP_200_OK, tags=[tag])
def get_petowners(db: Session = Depends(get_db)):
    return db.query(PetOwner).all()