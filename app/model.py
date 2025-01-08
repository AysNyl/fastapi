from typing import ClassVar
from .database import SQLModel, Field
from sqlmodel import Integer, String, Boolean, TIMESTAMP, Column, text
import datetime

class Post(SQLModel, table=True):
    __tablename__ = "posts1"
    # try this with class var:
    id: int = Field(primary_key=True, nullable=False)
    # title: str = Field(nullable=False)
    # comment: str = Field(nullable=False)
    # published: bool | None = Field(default=True)
    # id: ClassVar[Integer] = Column(Integer, primary_key=True, nullable=False)
    # title: ClassVar[String] = Column(String, nullable=False)
    # contenttr: ClassVar[String] = Column(String, nullable=False)
    # published: ClassVar[Boolean] = Column(Boolean, nullable=False, server_default="true")
    # createad_at: ClassVar[TIMESTAMP] = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    id: int = Field(sa_column=Column(Integer, primary_key=True, nullable=False, index=True))
    title: str = Field(sa_column=Column(String, nullable=False))
    content: str = Field(sa_column=Column(String, nullable=False))
    published: bool = Field(sa_column=Column(Boolean, nullable=False, server_default="true"))
    createad_at: datetime.datetime = Field(sa_column=Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")))