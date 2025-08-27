from pydantic import BaseModel


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class ProtectedResourceResponse(BaseModel):
    detail: str
