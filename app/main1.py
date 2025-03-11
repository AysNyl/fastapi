import time
from typing import Optional

import psycopg2
from fastapi import FastAPI, HTTPException, Response, status
from fastapi.params import Body
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel

from . import schemas


class Post(BaseModel):
    title: str
    content: str
    # published: Optional[bool] = True, tried to supply a null value
    # Python lets you write optional type hints 
    # where you can return either a specified type or None
    # to a column with not null constraint but with Default constraint
    # got an error, Explaination (stackoverflow):
    # DEFAULT is used if no value is passed and only on INSERT. 
    # NULL is a value, an unknown one but a value, 
    # so DEFAULT is not invoked and you trip the NOT NULL constraint. 
    # To get this to work just don't supply a value for the field.
    # conclusion: default is implicit
    published: bool = True


app = FastAPI()

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', 
                                password='admin123', cursor_factory=RealDictCursor)    
        cursor = conn.cursor()
        print('database connection was successfull!')
        break
    except Exception as error:
        print('Error: ', error)
        time.sleep(5)

@app.get("/")
async def root():
    return {'message': 'Hello World'}

@app.get("/posts")
async def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
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
async def add_post(add: schemas.PostCreate = Body(...)):
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
async def edit_post(id: int, update: Post = Body(...)):
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