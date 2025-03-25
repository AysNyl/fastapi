import datetime
from turtle import back

import pytz
from git import Optional
from numpy import True_, integer
from pydantic import EmailStr
from sqlalchemy import true
from sqlmodel import TIMESTAMP, Boolean, Column, Integer, Relationship, String, text
from tomlkit import table
from voluptuous import Email

from .database import Field, SQLModel


class User(SQLModel, table=True):
    __tablename__ = "users"
    id: int = Field(sa_column=Column(Integer, primary_key=True, nullable=False, index=True))
    email: EmailStr = Field(sa_column=Column(String, nullable=False))
    password: str = Field(sa_column=Column(String, nullable=False))
    created_at: datetime.datetime = Field(sa_column=Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")))
    posts: list["Post"] | None = Relationship(back_populates="user")


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

    # id: int = Field(sa_column=Column(Integer, primary_key=True, nullable=False, index=True))
    # user_id: int = Field(nullable=False, foreign_key="users.id")
    # title: str = Field(sa_column=Column(String, nullable=False))
    # content: str = Field(sa_column=Column(String, nullable=False))
    # published: bool = Field(sa_column=Column(Boolean, nullable=False, server_default="true"))
    # created_at: datetime.datetime = Field(sa_column=Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")))

    id: int = Field(primary_key=True, nullable=False, index=True)
    user_id: int = Field(nullable=False, foreign_key="users.id", ondelete="CASCADE")
    title: str = Field(nullable=False)
    content: str = Field(nullable=False)
    published: bool = Field(True, nullable=False)
    # created_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
    created_at: datetime.datetime = Field(sa_column=
                                          Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")))
    user: User | None = Relationship(back_populates="posts")


class Vote(SQLModel, table=True):
    __tablename__ = "votes"
    user_id: int = Field(nullable=False, foreign_key="users.id", ondelete="CASCADE", primary_key=True)
    post_id: int = Field(nullable=False, foreign_key="posts1.id", ondelete="CASCADE", primary_key=True)


class VoteIn(SQLModel):
    post_id: int
    check: bool = False


class ReUser(SQLModel):
    email: EmailStr
    registered: bool = True
    created_at: datetime.datetime
    # posts = list["RePost"] = Relationship(back_populates="user")


class UserLogin(SQLModel):
    email: EmailStr
    password: str


class RePost(SQLModel):
    user_id: int
    title: str
    content: str
    published: bool
    created_at: datetime.datetime
    # user: ReUser = Relationship(back_populates="posts")
    # votes: int


class PostOut(SQLModel):
    Post: RePost
    votes: int


class Token(SQLModel):
    access_token: str
    token_type: str


class TokenData(SQLModel):
    id: Optional[int] = None