from pydantic import BaseModel, Field


# from pydantic import field_validator


class User(BaseModel):
    id: int
    name: str
    age: int = Field(..., ge=0, le=150)

    # @field_validator('age')
    # @classmethod
    # def check_age(cls, v):
    #     if v <= 0:
    #         raise ValueError('Возраст должен быть положительным числом')
    #     return v
