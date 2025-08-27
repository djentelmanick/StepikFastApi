from functools import wraps

from fastapi import Request
from src.infrastructure.database import get_content_by_username
from src.presentation.api.exceptions import ForbiddenError, UnkownMethodError, UserNotFoundError
from src.presentation.api.schemas import User


class PermissionChecker:
    def __init__(self, roles: list[str]):
        self.roles = roles

    def __call__(self, func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            user: User = kwargs.get("user")
            if not user:
                raise UserNotFoundError

            if "admin" in user.roles:
                return await func(*args, **kwargs)

            if not any(role in user.roles for role in self.roles):
                raise ForbiddenError
            return await func(*args, **kwargs)

        return wrapper


class OwnershipChecker:
    def __call__(self, func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            user: User = kwargs.get("user")
            if not user:
                raise UserNotFoundError

            if "admin" in user.roles:
                return await func(*args, **kwargs)

            request = kwargs.get("request")
            viewed_username = kwargs.get("viewed_username")
            method = request.method if isinstance(request, Request) else None

            if method == "GET":
                content = get_content_by_username(viewed_username)

                if viewed_username == user.username or content.is_public:
                    return await func(*args, **kwargs)

                raise ForbiddenError

            if method in ("POST", "PUT", "DELETE"):
                if viewed_username == user.username:
                    return await func(*args, **kwargs)

                raise ForbiddenError

            raise UnkownMethodError

        return wrapper
