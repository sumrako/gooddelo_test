from fastapi import APIRouter, Depends
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.db import get_db
from schemas import Token, User, UserCreate
from services import authenticate_user, create_user
from exceptions import UnAuthorized, IncorrectToken, NotFoundToken
from utils import create_access_token
from datetime import timedelta
from app.settings import settings
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse
from jose import JWTError, jwt

security = HTTPBearer()
router = APIRouter()


@router.post("/logout")
def logout(credentials: HTTPAuthorizationCredentials = security):
    try:
        # Извлечение JWT-токена из заголовка авторизации
        token = credentials.credentials
        # Проверка валидности токена
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

        # Проверка, что токен находится в хранилище
        if token in token_storage:
            # Удаление токена из хранилища
            token_storage.remove(token)
            return JSONResponse(content={"message": "Пользователь разлогинен"}, status_code=200)
        else:
            raise IncorrectToken
    except JWTError:
        raise NotFoundToken


@router.post("/login", response_model=Token)
async def login(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise UnAuthorized
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register", response_model=User)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    response_user = create_user(db, user.username, user.password)
    return response_user
