from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel

from typing import Optional

def gen_num(initial: int = 0):
    while True:
        initial += 1
        yield initial

class Post(BaseModel):
    # id: int
    post: str
    published: bool = True
    rating: Optional[int] = None


def find_post(id):
    for post in posts:
        if post["id"] == id:
            return post

idgenerator = gen_num()

app = FastAPI()

posts = list()

@app.get("/")
async def root():
    return {'message': 'Hello Word'}

@app.get("/posts")
async def get_posts():
    return posts

@app.get("/posts/{id}")
async def get_posts(id: int):
    if not find_post(id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post does not exist")
    return find_post(id)

@app.post("/add_post", status_code=status.HTTP_201_CREATED)
async def add_post(add: Post = Body(...)):
    post = add.model_dump()
    post["id"] = next(idgenerator)
    print(post)
    posts.append(post)
    return post

@app.put("/edit_post/{id}")
async def edit_post(id: int, edit: Post = Body(...)):
    find_post(id)
    print(edit.model_dump())
    return edit