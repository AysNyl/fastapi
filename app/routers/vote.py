from typing import Annotated
from fastapi import APIRouter, Depends, status, HTTPException

from app.model import Vote, VoteIn
from app.utils import get_current_user

from app.database import SessionDep, select

router = APIRouter(
    tags = ['Vote'],
    prefix = "/vote"
)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def vote(session: SessionDep, current_user: Annotated[int, Depends(get_current_user)], vote: VoteIn):
    statement = select(Vote).where(Vote.user_id == current_user, Vote.post_id == vote.post_id)

    if not session.exec(statement=statement).first():
        if vote.check:
            add_vote = Vote(user_id=current_user, post_id=vote.post_id)
            session.add(add_vote)
            session.commit()
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    else:
        if not vote.check:
            delete_vote = session.exec(statement=statement).one()
            session.delete(delete_vote)
            session.commit()
        else:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="already checked")

