from fastapi import APIRouter, Depends
from src.core.enum import UserRole
from src.presentation.api.rbac import PermissionChecker
from src.presentation.api.schemas import User
from src.presentation.api.utils import get_user_from_token, role_based_rate_limit

router = APIRouter(prefix="/user", tags=["Protected"])


@router.get("", dependencies=[Depends(role_based_rate_limit)])
@PermissionChecker([UserRole.USER])
async def user_info(
    user: User = Depends(get_user_from_token),
) -> User:
    return user
