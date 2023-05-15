from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import Response
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError, jwt
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from fastapi.exceptions import HTTPException

import auth.services as services
from app.db import get_db, redis_client, Base, engine
from app.settings import settings
from auth.exceptions import UnAuthorized, IncorrectToken, NotFoundToken, DatabaseError, NotFoundData
from auth.schemas import Token, User, UserCreate, Task, TaskUpdate, TaskCreate, TaskList
from auth.utils import create_access_token

security = HTTPBearer()
router = APIRouter()

Base.metadata.create_all(bind=engine)

MAX_LIMIT = 10000


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username = payload.get("sub")
        if username is None or not redis_client.exists(credentials.credentials):
            raise JWTError
    except JWTError as e:
        raise HTTPException(status_code=401, detail=(str(e)))
    return username


@router.post("/logout")
def logout(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        token = credentials.credentials
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        if redis_client.exists(token):
            redis_client.delete(token)
            return Response(status_code=200)
        else:
            raise IncorrectToken
    except JWTError:
        raise NotFoundToken


@router.post("/login", response_model=Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                db: Session = Depends(get_db)):
    user = services.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise UnAuthorized
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    redis_client.set(access_token, "access")
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register", response_model=User)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        user = services.create_user(db, user.username, user.password)
        return user
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/tasks", response_model=Task)
def create_task(task: TaskCreate, curr_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        created_task = services.create_task(db, task.title, task.user_id)
        return created_task
    except SQLAlchemyError:
        raise DatabaseError


@router.get("/tasks", response_model=TaskList)
def get_tasks(curr_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    tasks = services.get_tasks(db, limit=MAX_LIMIT, offset=0)
    if not tasks:
        raise NotFoundData
    return tasks


@router.get("/tasks/{task_id}", response_model=Task)
def get_task_by_id(task_id: int, curr_user: int = Depends(get_current_user), db: Session = Depends(get_db)):
    tasks = services.get_tasks(db, ids=[task_id])
    if not tasks:
        raise NotFoundData
    return tasks[0]


@router.put("/tasks/{task_id}")
def put_task_by_id(task_id: int, task_data: TaskUpdate,
                   curr_user: int = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        services.update_task(db, task_id, task_data.title)
        return Response(status_code=204)
    except SQLAlchemyError:
        raise DatabaseError


@router.delete("/tasks/{task_id}")
def delete_task_by_id(task_id: int, curr_user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        services.delete_task(db, task_id)
        return Response(status_code=204)
    except SQLAlchemyError:
        raise DatabaseError

