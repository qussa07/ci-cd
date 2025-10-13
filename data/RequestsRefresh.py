from pydantic import BaseModel
from fastapi import Header

class RefreshRequest(BaseModel):
    refresh_token: str = Header(...)