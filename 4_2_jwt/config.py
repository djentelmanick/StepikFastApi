from dataclasses import dataclass

from environs import Env


@dataclass
class Config:
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int


def load_config(path: str = None) -> Config:
    env = Env()
    env.read_env(path)

    return Config(
        secret_key=env.str("SECRET_KEY"),
        algorithm=env.str("ALGORITHM", default="HS256"),
        access_token_expire_minutes=env.int("ACCESS_TOKEN_EXPIRE_MINUTES", default=10),
    )


config = load_config()
