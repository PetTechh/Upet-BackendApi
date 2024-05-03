
from config.db import get_db
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
from auth.schemas.auth import  Token
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from typing import Annotated
from passlib.context import CryptContext
from datetime import timedelta, datetime
from jose import JWTError, jwt
from schemas.user import UserSchemaPost
from models.user import User
from  passlib.hash import bcrypt as func

auth = APIRouter()

endpoint = "/auth/users"
tag = "Auth"
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = '197b2c371eas312ze#@1ssdsasd1123'
ALGORITHM = 'HS256'

@auth.post(endpoint, status_code=status.HTTP_201_CREATED, tags=[tag])
async def create_user(create_user_request: UserSchemaPost, db: Session=Depends(get_db)):

    existing_user = db.query(User).filter(User.email == create_user_request.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El correo electrónico ya está registrado.")

    if create_user_request.userType not in ["Vet", "Owner"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="UserType debe ser 'Vet' u 'Owner'.")

    new_user_data = {"name": create_user_request.name, 
                     "email": create_user_request.email, 
                     "userType": create_user_request.userType, 
                     "registered": False}
    new_user_data["password"] = func.encrypt(create_user_request.password.encode("utf-8"))


    new_user = User(**new_user_data)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)  # Refresh the user to get the updated data from the database

    return new_user



@auth.post(endpoint + "/token", response_model=Token, tags=[tag])
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    
    token = create_access_token(user.email, user.id, timedelta(hours=1))

    return {"access_token": token, "token_type": "bearer"}

def get_current_user(token: str = Depends(OAuth2PasswordBearer(tokenUrl="token"))):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        user_id: int = payload.get("id")
        if email is None or user_id is None:
            raise credentials_exception
        return {'email': email, 'user_id': user_id}
    except JWTError:
        raise credentials_exception


user_dependency = Annotated[dict, Depends(get_current_user)]
@auth.get(endpoint, status_code= status.HTTP_200_OK, tags=[tag])
async def get_users(user: user_dependency, db: Session = Depends(get_db)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    return {"User": user}


def authenticate_user(email: str, password: str, db):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.password):  
        return False
    return user

def create_access_token(email : str, user_id: int, expires_delta: timedelta):
    to_encode = {"sub": email, "user_id": user_id}
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

