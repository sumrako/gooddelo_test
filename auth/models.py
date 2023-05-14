import datetime

from sqlalchemy.types import TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    username = Column(String(255), nullable=False, index=True)
    hashed_password = Column(String, nullable=False, index=True)
    is_active = Column(Boolean, nullable=False, index=True, default=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, default=datetime.datetime.utcnow())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, default=datetime.datetime.utcnow())

    tasks = relationship("Task", back_populates="user")


class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, default=datetime.datetime.utcnow())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, default=datetime.datetime.utcnow())

    user = relationship("User", back_populates="tasks")