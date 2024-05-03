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

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl=token_url)

class AuthServices:

    def authenticate_user(self, email: str, password: str, db):
        user = db.query(User).filter(User.email == email).first()
        if not user:
            return False
        if not bcrypt_context.verify(password, user.password):  
            return False
        
        return user

    def create_access_token(self, email : str, user_id: int, expires_delta: timedelta):
        to_encode = {"sub": email, "user_id": user_id}
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
            user_id: int = payload.get("id")
            if email is None or user_id is None:
                raise credentials_exception
            return {'email': email, 'user_id': user_id}
        except JWTError:
            raise credentials_exception
        

