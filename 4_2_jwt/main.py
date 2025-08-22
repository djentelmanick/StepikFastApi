from config import token_type
from crypt_context import get_password_hash
from db import add_user
from fastapi import Body, Depends, FastAPI, Request, Response, status
from schemas import Token, User, UserInDB
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from utils import auth_user, create_token, get_user_from_access_token, get_user_from_refresh_token


limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@app.post("/login", tags=["User"])
@limiter.limit("5/minute")
async def login(request: Request, user: UserInDB = Depends(auth_user)):
    data = {"sub": user.username}
    return {
        "access_token": create_token(data=data),
        "refresh_token": create_token(data=data, type_token=token_type.refresh),
        "token_type": "bearer",
    }


@app.get("/protected_resource", tags=["User"])
async def protected_resource(username: str = Depends(get_user_from_access_token)):
    return {"message": f"Hello, {username}! Your token is valid"}


@app.post("/register", tags=["User"])
@limiter.limit("1/minute")
async def register(request: Request, user: User, response: Response):
    add_user(UserInDB(username=user.username, hashed_password=get_password_hash(user.password)))
    response.status_code = status.HTTP_201_CREATED
    return {"message": "User created successfully"}


@app.post("/refresh", tags=["User"])
@limiter.limit("5/minute")
async def refresh(request: Request, response: Response, token: Token = Body(...)):
    data = {"sub": get_user_from_refresh_token(token.refresh_token)}
    return {
        "access_token": create_token(data=data),
        "refresh_token": create_token(data=data, type_token=token_type.refresh),
        "token_type": "bearer",
    }
