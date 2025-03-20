from typing import Any

from fastapi import APIRouter, HTTPException, status
from fastapi.params import Body

# '.' represent './' for relative imports
from ..database import SessionDep, select
from ..model import ReUser, User
from ..utils import hash

router = APIRouter(
    tags = ['Users']
)

@router.post("/register", response_model=ReUser, status_code=status.HTTP_201_CREATED)
async def register(session: SessionDep, user: User = Body(...)) -> Any:

    # hash the password
    user.password = hash(user.password)

    new_user = User(**user.model_dump())
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return new_user

@router.get("/user/{id}", response_model=ReUser)
async def get_user(id: int, session: SessionDep):
    get_user = session.exec(select(User).filter(User.id == id)).first()
    if not get_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="user id {} not found".format(id))
    return get_user
    