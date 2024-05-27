import random
import string
import datetime
from sqlalchemy.orm import Session
from models.otps import OTP
from config.db import get_db
from fastapi import Depends
from fastapi import HTTPException, status
from models.petOwner import PetOwner
from models.pet import Pet
from schemas.pet import PetSchemaPost, PetSchemaResponse
class PetServices:
    @staticmethod
    def create_new_pet(petowner_id: int, pet: PetSchemaPost, db: Session = Depends(get_db)):
        pet_owner = db.query(PetOwner).filter(PetOwner.id == petowner_id).first()
        if not pet_owner:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El propietario de la mascota no existe.")

        if pet.weight <= 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El peso debe ser mayor a 0.")

 
        new_pet = Pet(petOwnerId=petowner_id, 
                      name=pet.name, 
                      birthdate=pet.birthdate, 
                      weight=pet.weight, 
                      species=pet.species,
                        breed=pet.breed, 
                        gender= pet.gender,
                        image_url= pet.image_url)
        db.add(new_pet)
        db.commit()
        db.refresh(new_pet)  # Para cargar el ID generado
        return new_pet

    @staticmethod
    def get_petowners(db: Session = Depends(get_db)):
        pets = db.query(Pet).all()
        return pets

    
    @staticmethod
    def get_pet_by_user_id(pet_id: int, db: Session):
        pet = db.query(Pet).filter(Pet.id == pet_id).first()
        return pet

    @staticmethod
    def get_pets_by_petOwnerid(petOwner_id: int, db: Session):
        pets = db.query(Pet).filter(Pet.petOwnerId == petOwner_id).all()
        return pets
    
    @staticmethod
    def update_pet(pet_id: int, pet: PetSchemaPost, db: Session):
        pet_db = db.query(Pet).filter(Pet.id == pet_id).first()
        if not pet_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mascota no encontrada")
  
        PetSchemaResponse.update_pet_from_schema(pet_db, pet)
        db.commit()
        return pet_db
    
    @staticmethod
    def delete_pet(pet_id: int, db: Session):
        pet = db.query(Pet).filter(Pet.id == pet_id).first()
        if not pet:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mascota no encontrada")
        db.delete(pet)
        db.commit()
        return pet
       
