from typing import Annotated
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from app import utils
from app.model import Token, User, UserLogin
from ..database import SessionDep, select

router = APIRouter(
    tags = ['Authentication']
)

@router.get("/login")
async def login(log: Annotated[OAuth2PasswordRequestForm, Depends()], session: SessionDep):
    user = session.exec(select(User).filter(User.email == log.username)).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="Invalid Credentials")
    if not utils.verify(log.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail="Invalid Credentials")
    access_token = utils.create_access_token(data={"User_Id": user.id})
    return Token(access_token = access_token, token_type = "bearer")