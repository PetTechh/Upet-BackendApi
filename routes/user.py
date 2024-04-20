from fastapi import APIRouter, Depends, HTTPException, status
from config.db import get_db
from models.user import User, PetOwner, Veterinarian
from models.veterinaryClinic import VeterinaryClinic
from schemas.user import UserSchemaPost, UserSchemaGet, VeterinarianSchemaGet, VeterinarianSchemaPost, PetOwnerSchemaGet, PetOwnerSchemaPost, SubscriptionType
from cryptography.fernet import Fernet
from sqlalchemy.orm import Session

users = APIRouter()
tag = "users"

key = Fernet.generate_key()
func = Fernet(key)

@users.get("/users/", response_model=list[UserSchemaGet], status_code=status.HTTP_200_OK, tags=[tag])
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@users.post("/users/", response_model=UserSchemaGet, status_code=status.HTTP_201_CREATED, tags=[tag])
def create_user(user: UserSchemaPost, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El correo electrónico ya está registrado.")

    if user.userType not in ["Vet", "Owner"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="UserType debe ser 'Vet' u 'Owner'.")

    new_user_data = {"name": user.name, "email": user.email, "userType": user.userType, "registered": False}
    new_user_data["password"] = func.encrypt(user.password.encode("utf-8"))

    new_user = User(**new_user_data)
    db.add(new_user)
    db.commit()
    return new_user

@users.post("/users/veterinarian/{user_id}", response_model=VeterinarianSchemaPost, status_code=status.HTTP_201_CREATED, tags=[tag])
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

@users.post("/users/petowner/{user_id}", response_model=PetOwnerSchemaGet, status_code=status.HTTP_201_CREATED, tags=[tag])
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

@users.get("/users/petowners", response_model=list[PetOwnerSchemaGet], status_code=status.HTTP_200_OK, tags=[tag])
def get_petowners(db: Session = Depends(get_db)):
    return db.query(PetOwner).all()

@users.get("/users/veterinarians", response_model=list[VeterinarianSchemaGet], status_code=status.HTTP_200_OK, tags=[tag])
def get_veterinarians(db: Session = Depends(get_db)):
    return db.query(Veterinarian).all()
