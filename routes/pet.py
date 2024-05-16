from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from config.db import get_db
from models.petOwner import PetOwner

from schemas.pet import PetSchemaPost, PetSchemaResponse
from models.pet import Pet

pets = APIRouter()
tag = "Pets"
endpoint = "/pets"


@pets.post( endpoint + "/{petowner_id}", response_model=PetSchemaResponse, status_code=status.HTTP_201_CREATED, tags=[tag])
def create_pet(petowner_id: int, pet: PetSchemaPost, db: Session = Depends(get_db)):
    pet_owner = db.query(PetOwner).filter(PetOwner.id == petowner_id).first()
    if not pet_owner:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El propietario de la mascota no existe.")
    

    if pet.weight <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El peso debe ser mayor a 0.")
    
    new_pet = Pet(petOwnerId=petowner_id, **pet.dict())
    db.add(new_pet)
    db.commit()
    return new_pet


@pets.get( endpoint, response_model=list[PetSchemaResponse], status_code=status.HTTP_200_OK, tags=[tag])
def get_pets(db: Session = Depends(get_db)):
    return db.query(Pet).all()


@pets.get(  endpoint + "/{petowner_id}", response_model=list[PetSchemaResponse], status_code=status.HTTP_200_OK, tags=[tag])
def get_pets_by_owner(petowner_id: int, db: Session = Depends(get_db)):
    pet_owner = db.query(PetOwner).filter(PetOwner.id == petowner_id).first()
    if not pet_owner:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El propietario de la mascota no existe.")
    pets = db.query(Pet).filter(Pet.petOwnerId == petowner_id).all()
    return pets
