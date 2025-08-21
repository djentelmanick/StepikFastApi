from crypt_context import pwd_context
from db import fake_users_db
from fastapi import Depends, FastAPI
from schemas import User, UserInDB
from utils import auth_user


app = FastAPI()


@app.get("/login", tags=["User"])
async def auth(user: User = Depends(auth_user)):
    return "You got my secret, %s. Welcome!" % user.username


@app.post("/rigister", tags=["User"])
async def register(user: User):
    for user_db in fake_users_db:
        if user_db.username == user.username:
            return "User already exists"

    hashed_password = pwd_context.hash(user.password)
    fake_users_db.append(UserInDB(username=user.username, hashed_password=hashed_password))
    return "%s, you successfully registered!" % user.username
