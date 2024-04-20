from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from config.db import get_db
from models.user import PetOwner

from schemas.pet import PetSchemaPost, PetSchemaGet
from models.pet import Pet

pets = APIRouter()
tag = "pets"

@pets.post("/pets/", response_model=PetSchemaGet, status_code=status.HTTP_201_CREATED, tags=[tag])
def create_pet(pet: PetSchemaPost, db: Session = Depends(get_db)):
    pet_owner = db.query(PetOwner).filter(PetOwner.id == pet.petOwnerId).first()
    if not pet_owner:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El propietario de la mascota no existe.")
    
    if pet.age <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La edad debe ser mayor a 0.")
    
    if pet.weight <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El peso debe ser mayor a 0.")
    
    new_pet = Pet(**pet.dict())
    db.add(new_pet)
    db.commit()
    return new_pet


@pets.get("/pets/", response_model=list[PetSchemaGet], status_code=status.HTTP_200_OK, tags=[tag])
def get_pets(db: Session = Depends(get_db)):
    return db.query(Pet).all()
