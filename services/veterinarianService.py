from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from config.db import get_db
from models.user import User
from models.veterinarian import Veterinarian
from models.veterinaryClinic import VeterinaryClinic
from schemas.veterinarian import VeterinarianSchemaPost, VeterinarianSchemaGet
from typing import List
from services.userService import UserService
from auth.schemas.auth import UserType
from schemas.veterinarian import VeterinarianSchemaGetByID
class VeterinarianService:
    @staticmethod
    def create_new_veterinarian(user_id: int, veterinarian: VeterinarianSchemaPost, db: Session = Depends(get_db)):
        user = UserService.get_user_by_id(user_id, db)
        # Verificar que el userType sea Vet
        if user.userType != UserType.Vet:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no es un veterinario.")

        if user.registered== True:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario ya ha sido registrado")

        clinic = db.query(VeterinaryClinic).filter(VeterinaryClinic.id == veterinarian.clinicId).first()
        if not clinic:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="La clínica no existe.")

        new_veterinarian = Veterinarian(userId=user_id, clinicId=veterinarian.clinicId)
        db.add(new_veterinarian)
        user.registered = True
        db.commit()
        return new_veterinarian

    @staticmethod
    def get_veterinarians(db: Session = Depends(get_db)) -> List[VeterinarianSchemaGet]:
        return db.query(Veterinarian).all()

    @staticmethod
    def get_veterinarian_by_user_id(user_id: int, db: Session) -> VeterinarianSchemaGet:
        return db.query(Veterinarian).filter(Veterinarian.userId == user_id).first()
    
    @staticmethod
    def get_veterinarian_by_id(vet_id: int, db: Session) -> VeterinarianSchemaGetByID:
        
        veterinarian = db.query(Veterinarian).filter(Veterinarian.id == vet_id).first()
        if not veterinarian:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Veterinarian not found")
        
        user = db.query(User).filter(User.id == veterinarian.userId).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        return VeterinarianSchemaGetByID(id=veterinarian.id, name=user.name, clinicId=veterinarian.clinicId)