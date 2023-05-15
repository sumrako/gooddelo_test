from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from auth.exceptions import NotFoundSQL
from auth.models import User, Task
from auth.utils import JWTAuth

jwt_auth = JWTAuth()


def authenticate_user(db: Session, username: str, password: str):
    user = get_users(db, username=username)[0]
    if not (user or jwt_auth.verify_password(password, user.hashed_password)):
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
    hashed_password = jwt_auth.pwd_context.hash(password)
    db_user = User(username=username, hashed_password=hashed_password)
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except SQLAlchemyError as e:
        db.rollback()
        raise e


def get_tasks(db: Session, ids: list[int] = None,
              title: str = None,
              limit: int = 10,
              offset: int = 0):
    queryset = db.query(Task)
    if not (title is None):
        queryset = queryset.filter(Task.title == title)
    if not (ids is None):
        queryset = queryset.filter(Task.id.in_(ids))

    return queryset.limit(limit).offset(offset).all()


def create_task(db: Session, title: str, user_id: int):
    db_task = Task(title=title, user_id=user_id)
    try:
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return db_task
    except SQLAlchemyError as e:
        db.rollback()
        raise e


def update_task(db: Session, task_id: int, title: str):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise NotFoundSQL

    task.title = title
    try:
        db.commit()
        db.refresh(task)
    except SQLAlchemyError:
        db.rollback()
        raise SQLAlchemyError
    finally:
        db.close()


def delete_task(db: Session, task_id: int):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise NotFoundSQL

    try:
        db.delete(task)
        db.commit()
        return {"message": "Задача успешно удалена"}
    except SQLAlchemyError as e:
        db.rollback()
        raise SQLAlchemyError
    finally:
        db.close()
