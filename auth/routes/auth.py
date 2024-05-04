
from config.db import get_db
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
from auth.schemas.auth import  Token
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from datetime import timedelta
from schemas.user import UserSchemaPost
from models.user import User
from  passlib.hash import bcrypt as func
from auth.services.auth import AuthServices
from ..config.auth import token_endpoint, tag, endpoint
from schemas.auth import CreateUserRequest
auth = APIRouter()

auth_services = AuthServices()

@auth.post(endpoint + '/sign-up', status_code=status.HTTP_201_CREATED, tags=[tag])
async def sign_up(create_user_request: UserSchemaPost, db: Session=Depends(get_db)):

    existing_user = db.query(User).filter(User.email == create_user_request.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email registered. Please use another email or sign in if you already have an account.")

    if create_user_request.userType not in ["Vet", "Owner"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="UserType must be 'Vet' u 'Owner'.")

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




@auth.post(token_endpoint, status_code=status.HTTP_200_OK, response_model=Token, tags=[tag])
async def sign_in(create_user_request: CreateUserRequest, db: Session = Depends(get_db)):
    user = auth_services.authenticate_user(create_user_request.email, create_user_request.password, db)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    token = auth_services.create_access_token(user.email, user.id, timedelta(hours=1))

    return {"access_token": token, "token_type": "bearer"}


user_dependency = Annotated[dict, Depends(auth_services.get_current_user)]
@auth.get(endpoint + '/current-user', status_code= status.HTTP_200_OK, tags=[tag])
async def get_users(user: user_dependency, db: Session = Depends(get_db)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    return {"User": user}


