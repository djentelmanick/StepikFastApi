from environs import Env
from src.config.base import PATH_TO_ENV, Enviroment
from src.config.testing import DevelopmentConfig

env = Env()
env.read_env(path=PATH_TO_ENV)


class UnknownEnviroment(Exception):
    pass


def get_settings() -> DevelopmentConfig:
    type_env = env("ENV")
    if type_env == Enviroment.PROD:
        pass
    if type_env == Enviroment.TEST:
        return DevelopmentConfig()
    raise UnknownEnviroment


settings = get_settings()
