from enum import StrEnum

from pydantic import Field
from pydantic_settings import BaseSettings

PATH_TO_ENV = "4_3_rbac/.env"


class BaseConfig(BaseSettings):
    env: str = Field(alias="ENV")

    class Config:
        env_file = PATH_TO_ENV
        env_file_encoding = "utf-8"
        extra = "ignore"


class Enviroment(StrEnum):
    PROD = "prod"
    TEST = "test"
