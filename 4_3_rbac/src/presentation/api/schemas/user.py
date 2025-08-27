from pydantic import BaseModel, EmailStr


class User(BaseModel):
    username: str
    full_name: str | None = None
    email: EmailStr | None = None
    disabled: bool = False
    roles: list[str]


class UserWithPassword(User):
    hashed_password: str


class Resource(BaseModel):
    content: str
    is_public: bool = False
