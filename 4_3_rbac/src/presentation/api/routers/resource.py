from fastapi import APIRouter, Depends, Path, Request
from src.core.enum import UserRole
from src.infrastructure.database import (
    create_content_by_username,
    delete_content_by_username,
    get_content_by_username,
    update_content_by_username,
)
from src.presentation.api.rbac import OwnershipChecker, PermissionChecker
from src.presentation.api.schemas import ProtectedResourceResponse, Resource, User
from src.presentation.api.utils import get_user_from_token, role_based_rate_limit

router = APIRouter(prefix="/protected_resource", tags=["Protected resource"])


@router.get("/{viewed_username}", dependencies=[Depends(role_based_rate_limit)])
@PermissionChecker([UserRole.ADMIN, UserRole.USER, UserRole.GUEST])
@OwnershipChecker()
async def get_protected_resource(
    request: Request,
    viewed_username: str = Path(...),
    user: User = Depends(get_user_from_token),
) -> Resource:
    return get_content_by_username(viewed_username)


@router.post("/{viewed_username}", dependencies=[Depends(role_based_rate_limit)])
@PermissionChecker([UserRole.ADMIN, UserRole.USER])
@OwnershipChecker()
async def post_protected_resource(
    request: Request,
    resource: Resource,
    viewed_username: str = Path(...),
    user: User = Depends(get_user_from_token),
) -> ProtectedResourceResponse:
    create_content_by_username(viewed_username, resource)
    return ProtectedResourceResponse(detail="Resource created successfully")


@router.put("/{viewed_username}", dependencies=[Depends(role_based_rate_limit)])
@PermissionChecker([UserRole.ADMIN, UserRole.USER])
@OwnershipChecker()
async def put_protected_resource(
    request: Request,
    resource: Resource,
    viewed_username: str = Path(...),
    user: User = Depends(get_user_from_token),
) -> ProtectedResourceResponse:
    update_content_by_username(viewed_username, resource)
    return ProtectedResourceResponse(detail="Resource updated successfully")


@router.delete("/{viewed_username}", dependencies=[Depends(role_based_rate_limit)])
@PermissionChecker([UserRole.ADMIN, UserRole.USER])
@OwnershipChecker()
async def delete_protected_resource(
    request: Request,
    viewed_username: str = Path(...),
    user: User = Depends(get_user_from_token),
) -> ProtectedResourceResponse:
    delete_content_by_username(viewed_username)
    return ProtectedResourceResponse(detail="Resource deleted successfully")
