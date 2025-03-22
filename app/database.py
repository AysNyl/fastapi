from typing import Annotated    

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, and_, create_engine, select, or_, and_

"""postgresql://<username>:<password>
@<ip-address/hostname>/<database_name>"""
SQLModel_DATABASE_URL = "postgresql://postgres:admin123@localhost/fastapi"

engine = create_engine(SQLModel_DATABASE_URL, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(bind=engine, autocommit=False, autoflush=False) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]