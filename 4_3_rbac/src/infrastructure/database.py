from secrets import compare_digest

from src.core.crypt_context import get_password_hash
from src.core.enum import UserRole
from src.presentation.api.exceptions import ResourceAlreadyExistsError, ResourceNotFoundError, UserNotFoundError
from src.presentation.api.schemas import Resource, User, UserWithPassword

USER_DATA = [
    {
        "username": "admin",
        "hashed_password": get_password_hash("adminpass"),
        "roles": [UserRole.ADMIN],
        "full_name": "Admin User",
        "email": "admin@example.com",
        "disabled": False,
    },
    {
        "username": "user",
        "hashed_password": get_password_hash("userpass"),
        "roles": [UserRole.USER],
        "full_name": "Regular User",
        "email": "user@example.com",
        "disabled": False,
    },
    {
        "username": "guest",
        "hashed_password": get_password_hash("guestpass"),
        "roles": [UserRole.GUEST],
        "full_name": "Guest User",
        "email": "guest@example.com",
        "disabled": False,
    },
]

USER_CONTENT = {
    "alice": {"content": "Секретные данные Алисы", "is_public": False},
    "bob": {"content": "Публичные заметки Боба", "is_public": True},
    "admin": {"content": "Админский ресурс", "is_public": False},
    "user": {"content": "Публичные заметки Юзера", "is_public": False},
    "guest": {"content": "Гостьские заметки", "is_public": False},
    "anonymous": {"content": "Анонимные заметки", "is_public": True},
}


def get_user_by_username(username: str, with_password: bool = False) -> UserWithPassword | User | None:
    for user in USER_DATA:
        if compare_digest(user["username"], username):
            if with_password:
                return UserWithPassword(**user)
            return User(**user)
    raise UserNotFoundError


def get_content_by_username(username: str) -> Resource:
    if username not in USER_CONTENT:
        raise ResourceNotFoundError
    return Resource(**USER_CONTENT.get(username))


def create_content_by_username(username: str, resource: Resource) -> None:
    if username in USER_CONTENT:
        raise ResourceAlreadyExistsError
    USER_CONTENT[username] = {
        "content": resource.content,
        "is_public": resource.is_public,
    }


def update_content_by_username(username: str, resource: Resource) -> None:
    if username not in USER_CONTENT:
        raise ResourceNotFoundError
    USER_CONTENT[username] = {
        "content": resource.content,
        "is_public": resource.is_public,
    }


def delete_content_by_username(username: str) -> None:
    if username not in USER_CONTENT:
        raise ResourceNotFoundError
    del USER_CONTENT[username]
