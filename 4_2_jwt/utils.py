from datetime import datetime, timedelta, timezone

import jwt
from config import config
from crypt_context import pwd_context
from db import get_user_by_username
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from schemas import UserInDB


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def auth_user(form_data: OAuth2PasswordRequestForm = Depends()) -> UserInDB:
    user = get_user_by_username(form_data.username)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
            headers={"WWW-Authenticate": "Basic"},
        )

    if pwd_context.verify(form_data.password, user.hashed_password):
        return user

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Authorization failed",
        headers={"WWW-Authenticate": "Basic"},
    )


def create_access_token(data: dict, access_token_expires_minutes: int = config.access_token_expire_minutes) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=access_token_expires_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config.secret_key, algorithm=config.algorithm)
    return encoded_jwt


def get_user_from_token(token: str = Depends(oauth2_scheme)) -> dict:
    try:
        payload = jwt.decode(token, config.secret_key, algorithms=[config.algorithm])
        exp_timestamp = payload["exp"]
        exp_datetime = datetime.fromtimestamp(exp_timestamp)
        print(exp_datetime)
        return payload.get("sub")
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer", "X-Error-Redirect": "/login"},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
