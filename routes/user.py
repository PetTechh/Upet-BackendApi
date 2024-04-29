from fastapi import APIRouter, Depends, HTTPException, status
from config.db import get_db

from models.user import User

from schemas.user import UserSchemaPost, UserSchemaGet

from cryptography.fernet import Fernet
from sqlalchemy.orm import Session

users = APIRouter()
tag = "Users"

key = Fernet.generate_key()
func = Fernet(key)

endpoint = "/users"


@users.get(f"{endpoint}/auth/singin", response_model=list[UserSchemaGet], status_code=status.HTTP_200_OK, tags=[tag])
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@users.post(f"{endpoint}/auth/singup", response_model=UserSchemaGet, status_code=status.HTTP_201_CREATED, tags=[tag])
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
