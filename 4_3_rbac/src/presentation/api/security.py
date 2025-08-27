from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from src.config import settings
from src.core.crypt_context import verify_password
from src.infrastructure.database import get_user_by_username
from src.presentation.api.exceptions import AuthError, TokenExpiredError, TokenInvalidError, UserNotFoundError
from src.presentation.api.schemas import User, UserWithPassword

ouath2_scheme = OAuth2PasswordBearer(tokenUrl=settings.app.path_prefix + "/login")


def auth_user(form_data: OAuth2PasswordRequestForm = Depends()) -> User:
    print(form_data)
    user: UserWithPassword = get_user_by_username(form_data.username, with_password=True)

    if not user:
        raise UserNotFoundError

    if verify_password(form_data.password, user.hashed_password):
        print(user)
        return User(**user.model_dump())

    raise AuthError


def create_access_token(username: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.app.access_token_expire_minutes)
    payload = {
        "exp": expire,
        "sub": username,
    }
    return jwt.encode(payload, settings.app.secret_key, algorithm=settings.app.algorithm)


def get_username_from_token(token: str = Depends(ouath2_scheme)) -> str:
    try:
        payload = jwt.decode(token, settings.app.secret_key, algorithms=[settings.app.algorithm])
        return payload.get("sub")
    except jwt.ExpiredSignatureError:
        raise TokenExpiredError
    except jwt.InvalidTokenError:
        raise TokenInvalidError
