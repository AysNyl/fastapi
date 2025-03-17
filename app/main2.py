import time
from typing import Optional, Any

import psycopg2
from fastapi import FastAPI, HTTPException, Response, status
from fastapi.params import Body
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel

# '.' represent './' for relative imports
from .model import Post, User, RePost, ReUser
# use them with out of library module otherwise import will fail
from .database import SessionDep, create_db_and_tables, select

app = FastAPI()

# model.SQLModel.metadata.create_all(bind=engine)
create_db_and_tables()


"""https://fastapi.tiangolo.com/tutorial/dependencies/#dependencies"""
@app.get("/")
async def root(session: SessionDep):
    print(session.exec(select(Post)))
    return {'status': 'success'}

@app.get("/posts")
async def get_posts(session: SessionDep):
    posts = session.exec(select(Post)).all()
    print(posts)
    return {"all posts": posts}

@app.get("/post/{id}")
async def get_post(id: int, session: SessionDep):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (id,))
    # post = cursor.fetchone()
    post = session.exec(select(Post).where(Post.id == id)).one()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="post with id {} does not exist".format(id))
    return {"fetched post": post}

@app.post("/add_post", status_code=status.HTTP_201_CREATED)
async def add_post(session: SessionDep, schema: Post = Body(...)):
    new_post = Post(title=schema.title, content=schema.content, published=schema.published)
    session.add(new_post)
    session.commit()
    session.refresh(new_post)
    print(new_post)
    return {"added post": new_post}

@app.delete("/delete_post/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, session: SessionDep):
    # cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", (id,))
    # deleted_post = cursor.fetchone()
    # if not deleted_post:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                         detail="post not found")
    # conn.commit()
    statement = select(Post).where(Post.id == id)
    results = session.exec(statement)
    deleted_post = results.one()  # previous 3 lines could have been combined
    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="post with id {} does not exist".format(id))
    session.delete(deleted_post)
    session.commit()
    return {"deleted post": deleted_post}

@app.put("/edit_post/{id}")
async def edit_post(id: int, session: SessionDep, update: Post = Body(...)):
    # cursor.execute("""UPDATE posts SET 
    #                title = %s, content = %s, published = %s
    #                WHERE id = %s RETURNING *""",
    #                (update.title, update.content, update.published, id))
    # updated_post = cursor.fetchone()
    # conn.commit()
    statement = select(Post).where(Post.id == id)
    results = session.exec(statement)
    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                      detail="post with id {} does not exist".format(id))
    update_post = results.one()
    update_post.title = update.title if update.title else update_post.title
    update_post.content = update.content if update.content else update_post.content
    session.add(update_post)
    session.commit()
    session.refresh(update_post)
    return {"updated post": update_post}

@app.post("/register", status_code=status.HTTP_201_CREATED, response_model=ReUser)
def register(user: User, session: SessionDep) -> Any:
    new_user = User(**user.model_dump())
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    print(new_user)
    return new_user
