from pydantic import BaseModel
from fastapi import Header

class RefreshRequest(BaseModel):
    refresh_token: str = Header(...)
    refresh_token = refresh_token.replace("Bearer ", "")