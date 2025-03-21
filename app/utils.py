from datetime import datetime, timedelta, timezone
from email import header
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
import jwt
from jwt.exceptions import PyJWTError

from app.model import TokenData

SECRET_KEY = "3cc90f581523c6980ce02c627e648d8057a5a3e122d150592d5e3c102634d13e"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def hash(password: str):
    return pwd_context.hash(password)

def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_token

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, key=SECRET_KEY, algorithms=ALGORITHM)
        print("is this the error")
        id: int = payload.get("User_Id")
        print(id, type(id))

        if id is None:
            raise credentials_exception
        token_data = TokenData(id=id)
    except PyJWTError:
        raise credentials_exception
    
    return token_data
    
def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    print(token)
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                          detail="Could not validate credentials", 
                                          headers={"WWW-Authenticate": "Bearer"}
                                          )
    data = verify_access_token(token, credentials_exception)
    return data.id 
