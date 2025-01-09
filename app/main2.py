import time
from turtle import title
from typing import Optional

import psycopg2
from fastapi import FastAPI, HTTPException, Response, status
from fastapi.params import Body
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel
from requests import Session

# '.' represent './' for relative imports
from .model import Post
# use them with out of library module otherwise import will fail
from .database import SessionDep, create_db_and_tables, select

app = FastAPI()

# model.SQLModel.metadata.create_all(bind=engine)
create_db_and_tables()


"""https://fastapi.tiangolo.com/tutorial/dependencies/#dependencies"""
@app.get("/")
async def root(schema: Post, session: SessionDep):
    return {'status': 'success'}

@app.get("/posts")
async def get_posts(session: SessionDep):
    posts = session.exec(select(Post)).all()
    print(posts)
    return {"all posts": posts}

@app.get("/post/{id}")
async def get_post(session: SessionDep, id: int):
    post = session.exec(select(Post).where(Post.id == id)).one()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="post with id {} does not exist".format(id))
    return {"fetched post": post}

@app.post("/add_post", status_code=status.HTTP_201_CREATED)
async def add_post(session: SessionDep, schema: Post = Body(...)):
    new_post = Post(title=schema.title,
                    content=schema.content,
                    published=schema.published)
    session.add(new_post)
    session.commit()
    session.refresh(new_post)
    print(new_post)
    return {"added post": new_post}

@app.delete("/delete_post/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(session: SessionDep, id: int):
    delete_post = session.exec(select(Post).where(Post.id == id)).first()
    if not delete_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="post not found")
    session.delete(delete_post)
    session.commit()
    return {"deleted post": delete_post}
    

@app.put("/edit_post/{id}")
async def edit_post(session: SessionDep, id: int, update: Post = Body(...)):
    updated_post = session.exec(select(Post).where(Post.id == id)).first()
    if not updated_post:
        HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                      detail="post with id {} does not exist".format(id))
    updated_post = update
    session.add(updated_post)
    session.commit()
    session.refresh(updated_post)
    return {"updated post": updated_post}