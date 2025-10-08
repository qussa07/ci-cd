from typing import Union

import pydantic
import sqlalchemy
from pydantic import BaseModel, EmailStr

from data.db_session import SqlAlchemyBase


class Users_B(BaseModel):
    name: str
    password: str
    email: EmailStr


class UserRead(BaseModel):
    id: int

    class Config:
        orm_mode = True

class Users(SqlAlchemyBase):
    __tablename__ = 'Users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    password = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    email = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)
