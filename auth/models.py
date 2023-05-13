import datetime

from sqlalchemy.types import TIMESTAMP
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class CustomUser(Base):
    __tablename__ = 'custom_user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, default=datetime.datetime.utcnow())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, default=datetime.datetime.utcnow())
