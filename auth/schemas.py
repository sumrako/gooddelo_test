from pydantic import BaseModel
from typing import Union, List


class Task(BaseModel):
    id: int
    title: str
    user_id: int

    class Config:
        orm_mode = True


class TaskUpdate(BaseModel):
    title: str


class TaskCreate(TaskUpdate):
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

