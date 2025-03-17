from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.params import Body

from app.utils import get_current_user

# '.' represent './' for relative imports
from ..database import SessionDep, select
from ..model import Post


router = APIRouter(
    tags = ['Posts']
)

@router.get("/posts", response_model = List[Post])
async def get_posts(session: SessionDep):
    posts = session.exec(select(Post)).all()
    print(posts)
    return posts

@router.get("/post/{id}")
async def get_post(session: SessionDep, id: int):
    post = session.exec(select(Post).where(Post.id == id)).one()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="post with id {} does not exist".format(id))
    return {"fetched post": post}

@router.post("/add_post", status_code=status.HTTP_201_CREATED)
async def add_post(session: SessionDep,  user_id: Annotated[int, Depends(get_current_user)], schema: Post = Body(...)):
    print(user_id)
    new_post = Post(title=schema.title,
                    content=schema.content,
                    published=schema.published)
    session.add(new_post)
    session.commit()
    session.refresh(new_post)
    print(new_post)
    return {"added post": new_post}

@router.delete("/delete_post/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(session: SessionDep, id: int):
    delete_post = session.exec(select(Post).where(Post.id == id)).first()
    if not delete_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="post not found")
    session.delete(delete_post)
    session.commit()
    return {"deleted post": delete_post}
    

@router.put("/edit_post/{id}")
async def edit_post(session: SessionDep, id: int, update: Post = Body(...)):
    updated_post = session.exec(select(Post).where(Post.id == id)).first()
    if not updated_post:
        HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                      detail="post with id {} does not exist".format(id))
    updated_post = update
    session.add(updated_post)
    session.commit()
    session.refresh(updated_post)
    return updated_post
