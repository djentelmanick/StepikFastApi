import json
from uuid import uuid4

import redis
from api.schemas import LoginRequest, UserResponse
from fastapi import Cookie, FastAPI, HTTPException, Response
from passlib.context import CryptContext


app = FastAPI()

redis_client = redis.Redis(host="localhost", port=6379, db=0)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@app.post("/login")
async def login(data: LoginRequest, response: Response):
    session_token = str(uuid4())
    hashed_password = pwd_context.hash(data.password)
    session_data = LoginRequest(username=data.username, password=hashed_password)
    redis_client.setex(session_token, 86400, session_data.model_dump_json())

    response.set_cookie(key="session_token", value=session_token, httponly=True, max_age=86400)
    return {"message": "Cookie has been set"}


@app.get("/user")
async def get_user(session_token: str = Cookie(None)):
    if not session_token:
        raise HTTPException(status_code=401, detail="Unauthorized")

    session_data = redis_client.get(session_token)
    if not session_data:
        raise HTTPException(status_code=401, detail="Session expired")

    try:
        user_data = json.loads(session_data)
        return UserResponse(**user_data)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid session data")
