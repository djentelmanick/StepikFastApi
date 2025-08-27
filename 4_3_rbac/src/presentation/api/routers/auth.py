from fastapi import APIRouter, Depends
from src.presentation.api.schemas import LoginResponse, User
from src.presentation.api.security import auth_user, create_access_token

router = APIRouter(prefix="/login", tags=["User"])


@router.post("")
async def login(user: User = Depends(auth_user)) -> LoginResponse:
    return LoginResponse(
        access_token=create_access_token(user.username),
        token_type="bearer",
    )
