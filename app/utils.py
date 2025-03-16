from datetime import datetime, timedelta
from passlib.context import CryptContext
import jwt
from jwt.exceptions import PyJWTError

SECRET_KEY = "3cc90f581523c6980ce02c627e648d8057a5a3e122d150592d5e3c102634d13e"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str):
    return pwd_context.hash(password)

def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_token

def verify_access_token(token: str, credentials_exception):
    payload = jwt.decode(token)
    id: str = payload.get("User_Id")

    if id is None:
        raise credentials_exception
    
