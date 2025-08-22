from secrets import compare_digest

from config import config
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


def verify_docs_credentials(credentials: HTTPBasicCredentials = Depends(security)):
    current_username_bytes = credentials.username.encode("utf8")
    correct_username_bytes = config.docs_user.encode("utf8")
    current_password_bytes = credentials.password.encode("utf8")
    correct_password_bytes = config.docs_password.encode("utf8")

    username_correct = compare_digest(current_username_bytes, correct_username_bytes)
    password_correct = compare_digest(current_password_bytes, correct_password_bytes)

    if not (username_correct and password_correct):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username
