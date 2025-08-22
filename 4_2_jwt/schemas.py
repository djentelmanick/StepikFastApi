from pydantic import BaseModel


class UserBase(BaseModel):
    username: str


class User(UserBase):
    password: str


class UserInDB(UserBase):
    hashed_password: str


class Token(BaseModel):
    refresh_token: str
