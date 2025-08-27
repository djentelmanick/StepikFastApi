from fastapi import Depends, Request, Response
from fastapi_limiter.depends import RateLimiter
from src.core.enum import RateLimitRole, UserRole
from src.infrastructure.database import get_user_by_username
from src.presentation.api.schemas import User
from src.presentation.api.security import get_username_from_token


def get_user_from_token(username: str = Depends(get_username_from_token)) -> User:
    return get_user_by_username(username)


async def role_based_rate_limit(
    request: Request,
    response: Response,
    current_user: User = Depends(get_user_from_token),
) -> RateLimiter:
    if UserRole.ADMIN in current_user.roles:
        limiter = RateLimiter(times=RateLimitRole.ADMIN, minutes=1)
    elif UserRole.USER in current_user.roles:
        limiter = RateLimiter(times=RateLimitRole.USER, minutes=1)
    else:
        limiter = RateLimiter(times=RateLimitRole.GUEST, minutes=1)
    await limiter(request=request, response=response)
