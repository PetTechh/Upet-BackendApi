from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from config.db import get_db
from models.user import User
from models.veterinarian import Veterinarian
from schemas.veterinarian import VeterinarianSchemaPost, VeterinarianSchemaGet
from typing import List
from services.userService import UserService
from auth.schemas.auth import UserType
from schemas.veterinarian import VeterinarianSchemaGet
from services.veterinaryClinicService import VeterinaryClinicService
from sqlalchemy.orm import joinedload
from auth.services.token import TokenServices
from auth.schemas.auth import Token
from datetime import timedelta


class VeterinarianService:

    @staticmethod
    def create_new_veterinarian(user_id: int, veterinarian: VeterinarianSchemaPost, db: Session):
        user = UserService.get_user_by_id(user_id, db)
        if user.userType != UserType.Vet:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no es un veterinario.")

        if user.registered == True:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario ya ha sido registrado")

        # Verificar OTP y obtener el clinicId
        clinic_id = VeterinaryClinicService.verify_veterinarian_register(clinic_name=veterinarian.clinicName, 
                                                                         otp_password=veterinarian.otp_password,
                                                                         db=db)

        new_veterinarian = Veterinarian(userId=user_id, clinicId=clinic_id)
    
        db.add(new_veterinarian)
        user.registered = True
        db.commit()
        
        token = TokenServices.create_access_token(user.email, new_veterinarian.id, user.userType, user.registered,timedelta(hours=1))

        return Token(access_token=token, token_type="bearer")

    @staticmethod
    def get_all_vets(db: Session = Depends(get_db)) -> List[VeterinarianSchemaGet]:
        vets = db.query(Veterinarian).options(joinedload(Veterinarian.user)).all()
        return [VeterinarianSchemaGet.from_orm(vet, vet.user) for vet in vets]

    @staticmethod
    def get_vet_by_user_id(user_id: int, db: Session) -> VeterinarianSchemaGet:
        veterinarian = (
            db.query(Veterinarian)
            .filter(Veterinarian.userId == user_id)
            .options(joinedload(Veterinarian.user))  # Carga la relación User junto con Veterinarian
            .first()
        )
        
        if not veterinarian:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Veterinarian not found")

        user = veterinarian.user
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        return VeterinarianSchemaGet.from_orm(veterinarian, user)

    @staticmethod
    def get_vet_by_id(vet_id: int, db: Session) -> VeterinarianSchemaGet:
        veterinarian = (
            db.query(Veterinarian)
            .filter(Veterinarian.id == vet_id)
            .options(joinedload(Veterinarian.user))  # Carga la relación User junto con Veterinarian
            .first()
        )
        
        if not veterinarian:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Veterinarian not found")

        user = veterinarian.user
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        return VeterinarianSchemaGet.from_orm(veterinarian, user)
    
    @staticmethod
    def get_vets_by_clinic_id(clinic_id: int, db: Session) -> List[VeterinarianSchemaGet]:
        vets = db.query(Veterinarian).filter(Veterinarian.clinicId == clinic_id).options(joinedload(Veterinarian.user)).all()
        return [VeterinarianSchemaGet.from_orm(vet, vet.user) for vet in vets]