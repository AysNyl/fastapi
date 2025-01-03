import time
from typing import Optional

import psycopg2
from fastapi import FastAPI, HTTPException, Response, status
from fastapi.params import Body
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel


class Post(BaseModel):
    title: str
    content: str
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
    return {'message': 'Hello Word'}

@app.get("/posts")
async def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    print(posts)
    return {"data": posts}

@app.get("/posts/{id}")
async def get_posts(id: int):
    if not find_post(id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post does not exist")
    return find_post(id)

@app.post("/add_post", status_code=status.HTTP_201_CREATED)
async def add_post(add: Post = Body(...)):
    cursor.execute("""INSERT INTO posts (title, content, published) 
                   VALUES (%s, %s, %s) RETURNING *""", 
                   (add.title, add.content, add.published))
    new_post = cursor.fetchone()
    print(new_post)
    return {"data": new_post}

@app.put("/edit_post/{id}")
async def edit_post(id: int, edit: Post = Body(...)):
    find_post(id)
    print(edit.model_dump())
    return edit