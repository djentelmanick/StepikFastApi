from typing import Literal

from pydantic import Field
from src.config.base import BaseConfig, Enviroment


class ApplicationConfig(BaseConfig):
    port: int = Field(alias="APP_PORT")
    host: str = Field(alias="APP_HOST")
    path_prefix: str = Field(alias="PATH_PREFIX")

    secret_key: str = Field(alias="ACCESS_TOKEN_SECRET_KEY")
    algorithm: str = Field(alias="ACCESS_TOKEN_ALGORITHM")
    access_token_expire_minutes: int = Field(alias="ACCESS_TOKEN_EXPIRE_MINUTES")

    internal_admin_username: str = Field(alias="INTERNAL_ADMIN_USERNAME")
    internal_admin_password: str = Field(alias="INTERNAL_ADMIN_PASSWORD")

    reload: bool = Field(alias="RELOAD_APP")


class DevelopmentConfig:
    app = ApplicationConfig()

    env: Literal[Enviroment.TEST] = Enviroment.TEST
