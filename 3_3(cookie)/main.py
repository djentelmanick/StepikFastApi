import json
from os import getenv
from uuid import uuid4

import redis
from api.schemas import LoginRequest, UserResponse
from dotenv import load_dotenv
from fastapi import Cookie, FastAPI, HTTPException, Response
from itsdangerous import BadSignature, Signer
from passlib.context import CryptContext


app = FastAPI()

redis_client = redis.Redis(host="localhost", port=6379, db=0)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

load_dotenv()
SECRET_KEY = getenv("SECRET_KEY")
signer = Signer(SECRET_KEY)


@app.post("/login")
async def login(data: LoginRequest, response: Response):
    user_id = str(uuid4())

    try:
        signed_token = signer.sign(user_id).decode("utf-8")
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to sign token")

    hashed_password = pwd_context.hash(data.password)
    session_data = {
        "user_id": user_id,
        "username": data.username,
        "password": hashed_password,
    }
    redis_client.setex(user_id, 65, json.dumps(session_data))

    response.set_cookie(key="session_token", value=signed_token, httponly=True, max_age=60)

    return {"message": "Cookie has been set"}


@app.get("/profile")
async def get_profile(session_token: str = Cookie(None)):
    if not session_token:
        raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        user_id = signer.unsign(session_token).decode("utf-8")
    except BadSignature:
        raise HTTPException(status_code=401, detail="Invalid session token")

    session_data = redis_client.get(user_id)
    if not session_data:
        raise HTTPException(status_code=401, detail="Session expired")

    try:
        user_data = json.loads(session_data)
        return UserResponse(**user_data)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid session data")
