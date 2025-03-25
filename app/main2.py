from fastapi import FastAPI, HTTPException, Response, status

# use them without of library module otherwise import will fail
from .database import SessionDep, create_db_and_tables, select
from .routers import post, user, auth, vote

app = FastAPI()

# model.SQLModel.metadata.create_all(bind=engine)
create_db_and_tables()


"""https://fastapi.tiangolo.com/tutorial/dependencies/#dependencies"""
@app.get("/")
async def root(session: SessionDep):
    return {'status': 'success'}

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)