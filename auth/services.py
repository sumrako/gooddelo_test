from sqlalchemy.orm import Session

from models import User
from utils import verify_password, pwd_context


def authenticate_user(db: Session, username: str, password: str):
    user = get_users(db, username=username)
    if not (user or verify_password(password, user.hashed_password)):
        return False

    return user


def get_users(db: Session, ids: list[int] = None,
              username: str = None,
              limit: int = 10,
              offset: int = 0):
    queryset = db.query(User)
    if not (username is None):
        queryset = queryset.filter(User.username == username)
    if not (ids is None):
        queryset = queryset.filter(User.id.in_(ids))

    return queryset.limit(limit).offset(offset).all()


def create_user(db: Session, username: str, password: str):
    hashed_password = pwd_context.hash(password)
    db_user = User(username=username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

