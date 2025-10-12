from datetime import datetime
from typing import Union
import pydantic
import sqlalchemy
from pydantic import BaseModel, EmailStr
from data.db_session import SqlAlchemyBase


class Re_tokenBase(BaseModel):
    user_id: int
    expires_at: datetime
    revoked: bool

    class Config:
        orm_mode = True

class Re_token(SqlAlchemyBase):
    __tablename__ = 'Re_token'

    id = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    expires_at = sqlalchemy.Column(sqlalchemy.Date, nullable=False)
    revoked = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
