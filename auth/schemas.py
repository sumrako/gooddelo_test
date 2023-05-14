from pydantic import BaseModel
from typing import Union


class Task(BaseModel):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class TaskCreate(BaseModel):
    title: str
    user_id: int


class UserCreate(BaseModel):
    username: str
    password: str


class User(BaseModel):
    id: int
    username: str
    is_active: bool
    tasks: list[Task] = []

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None
