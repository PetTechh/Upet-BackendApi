from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from config.db import get_db
from models.user import User
from passlib.hash import bcrypt as bcrypt_context
from typing import Annotated
from ..config.auth import SECRET_KEY, ALGORITHM, token_url
from schemas.user import UserType
from auth.schemas.auth import CreateUserRequest, UserSchemaPost
from auth.schemas.auth import  Token, UserSchemaResponse
from sqlalchemy.orm import Session
from services.veterinarianService import VeterinarianService
from services.petOwnerService import PetOwnerService
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl=token_url)

class AuthServices:
    @staticmethod
    def authenticate_user(email: str, password: str, db: Session):
        user = db.query(User).filter(User.email == email).first()
        if not user:
            return False
        if not bcrypt_context.verify(password, user.password):  
            return False
        
        return user

    @staticmethod
    def create_access_token( email : str, user_id: int, user_role: UserType , expires_delta: timedelta):
        to_encode = {"sub": email, "user_id": user_id, "user_role": user_role}
        expire = datetime.utcnow() + expires_delta
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    async def get_current_user(self, token: Annotated[str,Depends(oauth2_bearer)]):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            email: str = payload.get("sub")
            user_id: int = payload.get("user_id")
            if email is None or user_id is None:
                raise credentials_exception
            return {'email': email, 'user_id': user_id}
        except JWTError:
            raise credentials_exception
        
    @staticmethod
    async def sign_up(create_user_request: UserSchemaResponse, db: Session):
        existing_user = db.query(User).filter(User.email == create_user_request.email).first()
        if existing_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email registered. Please use another email or sign in if you already have an account.")

        if create_user_request.userType not in ["Vet", "Owner"]:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="UserType must be 'Vet' or 'Owner'.")

        new_user_data = {"name": create_user_request.name, 
                        "email": create_user_request.email, 
                        "userType": create_user_request.userType, 
                        "registered": False}
        new_user_data["password"] = bcrypt_context.encrypt(create_user_request.password.encode("utf-8"))

        new_user = User(**new_user_data)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)  # Refresh the user to get the updated data from the database

        return new_user

    @staticmethod
    async def sign_in(create_user_request: CreateUserRequest, db: Session):
        user = AuthServices.authenticate_user(create_user_request.email, create_user_request.password, db)
        role_id=0
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
            
        user_response = UserSchemaResponse(id=user.id, email=user.email, userType=user.userType, registered=user.registered, name=user.name)

        if user_response.registered == True:
            if user_response.userType == UserType.Vet:
                role_id = VeterinarianService.get_veterinarian_by_user_id(user_response.id, db).id
            elif user_response.userType == UserType.Owner:
                role_id = PetOwnerService.get_petowner_by_user_id(user_response.id, db).id
        else:
            role_id = user_response.id

        token = AuthServices.create_access_token(user_response.email, role_id, user_response.userType, timedelta(hours=1))

        return Token(access_token=token, token_type="bearer")