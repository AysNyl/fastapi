from .database import SQLModel, Field
from sqlmodel import Integer, String, Boolean

class Post(SQLModel, table=True):
    __tablename__ = "posts1"
    id: int = Field(primary_key=True, nullable=False)
    title: str = Field(nullable=False)
    comment: str = Field(nullable=False)
    published: bool = Field(default=True)