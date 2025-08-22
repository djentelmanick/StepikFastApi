from crypt_context import get_password_hash
from db import add_user
from fastapi import Depends, FastAPI, Request, Response, status
from schemas import User, UserInDB
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from utils import auth_user, create_access_token, get_user_from_token


limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@app.post("/login", tags=["User"])
@limiter.limit("5/minute")
async def login(request: Request, user: User = Depends(auth_user)):
    return {
        "access_token": create_access_token(data={"sub": user.username}),
        "token_type": "bearer",
    }


@app.get("/protected_resource", tags=["User"])
async def protected_resource(username: str = Depends(get_user_from_token)):
    return {"message": f"Hello, {username}! Your token is valid"}


@app.post("/register", tags=["User"])
@limiter.limit("1/minute")
async def register(request: Request, user: User, response: Response):
    add_user(UserInDB(username=user.username, hashed_password=get_password_hash(user.password)))
    response.status_code = status.HTTP_201_CREATED
    return {"message": "User created successfully"}
