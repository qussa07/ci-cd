from datetime import datetime, timedelta
from typing import Union, Optional
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
import sqlalchemy
from data.db_session import global_init, create_session
from pydantic import BaseModel
from data import db_session
from sqlalchemy.orm import Session
from argon2 import PasswordHasher
from data.userlogin import UserLogin
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from data.Users import Users_B, Users, UserRead



SECRET_KEY = "supersecretkey"  # ⚠️ вынеси в .env
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")

app = FastAPI()
global_init('db.db')
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def get_db():
    db = db_session.create_session()
    try:
        yield db
    finally:
        db.close()

# генерация JWT
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # адрес React
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/register", response_model=UserRead)
async def reg_user(item: Users_B, db_sess: Session = Depends(get_db)):
    if db_sess.query(Users).filter(Users.email == item.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    try:
        new_user = Users(
            name=item.name,
            email=item.email,
            password=hashed_password(item.password)
        )
        db_sess.add(new_user)
        db_sess.commit()
        db_sess.refresh(new_user)
    except sqlalchemy.exc.StatementError:
        raise HTTPException(status_code=400, error='Bad request')
    else:
        return new_user


@app.post("/api/login")
async def login_user(user: UserLogin, db_sess: Session = Depends(get_db)):
    db_user = db_sess.query(Users).filter(Users.email == user.email).first()
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid email or password")
    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid email or password")
    access_token = create_access_token(data={"sub": str(db_user.id)})
    return {"access_token": access_token, "token_type": "bearer"}


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(Users).filter(Users.id == int(user_id)).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user


@app.get("/api/me", response_model=UserRead)
def read_users_me(current_user: Users = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email
    }



def hashed_password(password):
    ph = PasswordHasher()
    return ph.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)


