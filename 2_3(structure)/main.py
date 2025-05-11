from fastapi import FastAPI
from src.api.endpoints.users import users


app = FastAPI()
app.include_router(users, tags=["users"])
