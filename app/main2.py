import time
from typing import Optional

import psycopg2
from fastapi import FastAPI, HTTPException, Response, status
from fastapi.params import Body
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel

# '.' represent './' for relative imports
from . import model
# use them with out of library module otherwise import will fail
from .database import SessionDep, create_db_and_tables, select

app = FastAPI()

# model.SQLModel.metadata.create_all(bind=engine)
create_db_and_tables()


"""https://fastapi.tiangolo.com/tutorial/dependencies/#dependencies"""
@app.get("/")
async def root(schema: model.Post, session: SessionDep):
    return {'status': 'success'}

@app.get("/posts")
async def get_posts(session: SessionDep):
    posts = session.exec(select(model.Post)).all()
    print(posts)
    return {"all posts": posts}

@app.get("/post/{id}")
async def get_post(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (id,))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="post with id {} does not exist".format(id))
    return {"fetched post": post}

@app.post("/add_post", status_code=status.HTTP_201_CREATED)
async def add_post(add: model.Post = Body(...)):
    # Run the query
    cursor.execute("""INSERT INTO posts (title, content, published) 
                   VALUES (%s, %s, %s) RETURNING *""", 
                   (add.title, add.content, add.published))
    # Capture the output of the query
    new_post = cursor.fetchone()
    # Commit the changes to actual database
    conn.commit()
    print(new_post)
    return {"added post": new_post}

@app.delete("/delete_post/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):
    cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", (id,))
    deleted_post = cursor.fetchone()
    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="post not found")
    conn.commit()
    return {"deleted post": deleted_post}
    

@app.put("/edit_post/{id}")
async def edit_post(id: int, update: model.Post = Body(...)):
    cursor.execute("""UPDATE posts SET 
                   title = %s, content = %s, published = %s
                   WHERE id = %s RETURNING *""",
                   (update.title, update.content, update.published, id))
    updated_post = cursor.fetchone()
    conn.commit()
    if not updated_post:
        HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                      detail="post with id {} does not exist".format(id))
    return {"updated post": updated_post}