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


@users.get(f"{endpoint}", response_model=list[UserSchemaGet], status_code=status.HTTP_200_OK, tags=[tag])
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()
