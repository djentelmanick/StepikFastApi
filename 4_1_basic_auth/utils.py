from secrets import compare_digest

from crypt_context import pwd_context
from db import fake_users_db
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials


security = HTTPBasic()


def auth_user(creds: HTTPBasicCredentials = Depends(security)):
    user = None
    for user_db in fake_users_db:
        if compare_digest(user_db.username, creds.username):
            user = user_db
            break

    if user and pwd_context.verify(creds.password, user.hashed_password):
        return user

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Basic"},
    )
