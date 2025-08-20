from secrets import compare_digest as safe_comp

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel


app = FastAPI()
security = HTTPBasic()


class User(BaseModel):
    username: str
    password: str


USERS = {
    "user1": User(username="user1", password="pass1"),
    "user2": User(username="user2", password="pass2"),
}


def auth_user(creds: HTTPBasicCredentials = Depends(security)):
    user = USERS.get(creds.username)
    if user and safe_comp(user.password, creds.password):
        return user

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Basic"},
    )


@app.get("/login", dependencies=[Depends(auth_user)])
async def auth():
    return "You got my secret, welcome"
