from datetime import datetime, timedelta, timezone

import jwt
from config import config, token_type
from crypt_context import pwd_context
from db import get_user_by_username
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from schemas import UserInDB


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
refresh_tokens = {}


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


def create_token(
    data: dict,
    access_token_expires_minutes: int = config.access_token_expire_minutes,
    type_token: str = token_type.access,
) -> str:
    to_encode = data.copy()

    expire = datetime.now(timezone.utc)
    if type_token == token_type.access:
        expire += timedelta(minutes=access_token_expires_minutes)
    elif type_token == token_type.refresh:
        expire += timedelta(days=config.refresh_token_expire_days) + timedelta(
            minutes=config.refresh_token_expire_minutes
        )

    to_encode.update({"exp": expire, "type": type_token})
    encoded_jwt = jwt.encode(to_encode, config.secret_key, algorithm=config.algorithm)

    if type_token == token_type.refresh:
        refresh_tokens[data.get("sub")] = encoded_jwt

    return encoded_jwt


def get_user_from_access_token(token: str = Depends(oauth2_scheme)) -> str:
    return _get_user_from_token(token, token_type.access)


def get_user_from_refresh_token(token: str = None) -> str:
    return _get_user_from_token(token, token_type.refresh)


def _get_user_from_token(token: str, type_token: str = token_type.access) -> str:
    try:
        payload = jwt.decode(token, config.secret_key, algorithms=[config.algorithm])
        exp_timestamp = payload.get("exp")
        exp_datetime = datetime.fromtimestamp(exp_timestamp)
        print(exp_datetime)
        username = payload.get("sub")

        if type_token == token_type.refresh and (
            payload.get("type") != token_type.refresh or refresh_tokens.get(username) != token
        ):
            raise jwt.InvalidTokenError

        if type_token == token_type.access and payload.get("type") != token_type.access:
            raise jwt.InvalidTokenError

        return username

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
