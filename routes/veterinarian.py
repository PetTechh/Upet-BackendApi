from fastapi import APIRouter, Depends, HTTPException, status
from config.db import get_db

from routes.user import endpoint as user_endpoint

from models.user import User
from models.veterinarian import Veterinarian
from models.veterinaryClinic import VeterinaryClinic

from schemas.veterinarian import VeterinarianSchemaGet, VeterinarianSchemaPost

from sqlalchemy.orm import Session

veterinarians = APIRouter()
tag = "Veterinarians"


endpoint = user_endpoint + "/veterinarians"

@veterinarians.post( endpoint + "/{user_id}", response_model=VeterinarianSchemaGet, status_code=status.HTTP_201_CREATED, tags=[tag])
def create_veterinarian(user_id: int, veterinarian: VeterinarianSchemaPost, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El usuario no existe o no es un veterinario no registrado.")
    
    # Verificar que el userType sea Vet
    if user.userType != "Vet":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no es un veterinario.")

    if user.registered== True:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario ya ha sido registrado")

    new_veterinarian = Veterinarian(userId=user_id, clinicId=veterinarian.clinicId)
    
    clinic = db.query(VeterinaryClinic).filter(VeterinaryClinic.id == veterinarian.clinicId).first()
    
    if not clinic:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="La clínica no existe.")
    
    db.add(new_veterinarian)
    user.registered = True
    db.commit()
    return new_veterinarian



@veterinarians.get(endpoint, response_model=list[VeterinarianSchemaGet], status_code=status.HTTP_200_OK, tags=[tag])
def get_veterinarians(db: Session = Depends(get_db)):
    return db.query(Veterinarian).all()
