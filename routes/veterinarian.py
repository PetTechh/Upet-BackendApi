from fastapi import APIRouter, Depends, HTTPException, status
from config.db import get_db


from models.user import User
from models.veterinarian import Veterinarian
from models.veterinaryClinic import VeterinaryClinic
from schemas.veterinarian import VeterinarianSchemaPost, VeterinarianSchemaGet, VeterinarianSchemaGetByID

from schemas.veterinarian import VeterinarianSchemaGet, VeterinarianSchemaPost

from sqlalchemy.orm import Session
from services.veterinarianService import VeterinarianService
veterinarians = APIRouter()
tag = "Veterinarians"


endpoint =  "/veterinarians"

@veterinarians.post( endpoint + "/{user_id}", response_model=VeterinarianSchemaGet, status_code=status.HTTP_201_CREATED, tags=[tag])
def create_veterinarian(user_id: int, veterinarian: VeterinarianSchemaPost, db: Session = Depends(get_db)):
    return VeterinarianService.create_new_veterinarian(user_id, veterinarian, db)




@veterinarians.get(endpoint, response_model=list[VeterinarianSchemaGet], status_code=status.HTTP_200_OK, tags=[tag])
def get_veterinarians(db: Session = Depends(get_db)):
    return VeterinarianService.get_veterinarians(db)

@veterinarians.get(endpoint + "/users/{user_id}", response_model=VeterinarianSchemaGet, tags=[tag])
def get_veterinarian_by_user_id(user_id: int, db: Session = Depends(get_db)):
    veterinarian = VeterinarianService.get_veterinarian_by_user_id(user_id, db)
    if not veterinarian:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Veterinarian not found")
    return veterinarian

@veterinarians.get(endpoint + "{vet_id}", response_model=VeterinarianSchemaGetByID, tags=[tag])
def get_veterinarian_by_id(vet_id: int, db: Session = Depends(get_db)):
    veterinarian = VeterinarianService.get_veterinarian_by_id(vet_id, db)
    return veterinarian