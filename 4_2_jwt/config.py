from dataclasses import dataclass

from environs import Env


@dataclass
class Config:
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    refresh_token_expire_minutes: int
    refresh_token_expire_days: int


def load_config(path: str = None) -> Config:
    env = Env()
    env.read_env(path)

    return Config(
        secret_key=env.str("SECRET_KEY"),
        algorithm=env.str("ALGORITHM", default="HS256"),
        access_token_expire_minutes=env.int("ACCESS_TOKEN_EXPIRE_MINUTES", default=15),
        refresh_token_expire_minutes=env.int("REFRESH_TOKEN_EXPIRE_MINUTES", default=0),
        refresh_token_expire_days=env.int("REFRESH_TOKEN_EXPIRE_DAYS", default=7),
    )


config = load_config()


@dataclass
class TokenType:
    access: str = "access"
    refresh: str = "refresh"


token_type = TokenType()
