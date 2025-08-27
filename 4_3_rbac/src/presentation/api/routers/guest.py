from fastapi import APIRouter, Depends, Request
from src.core.enum import UserRole
from src.presentation.api.rbac import PermissionChecker
from src.presentation.api.schemas import User
from src.presentation.api.utils import get_user_from_token, role_based_rate_limit

router = APIRouter(prefix="/guest", tags=["Protected"])


@router.get("", dependencies=[Depends(role_based_rate_limit)])
@PermissionChecker([UserRole.GUEST])
async def guest_info(
    request: Request,
    user: User = Depends(get_user_from_token),
) -> User:
    return user
