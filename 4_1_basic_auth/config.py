from dataclasses import dataclass

from environs import Env


@dataclass
class Config:
    mode: str
    docs_user: str
    docs_password: str


def load_config(path: str = None) -> Config:
    env = Env()
    env.read_env(path)

    mode = env.str("MODE")
    if mode not in ["DEV", "PROD"]:
        raise ValueError("Invalid mode")

    return Config(
        mode=mode,
        docs_user=env.str("DOCS_USER"),
        docs_password=env.str("DOCS_PASSWORD"),
    )


config = load_config()

if __name__ == "__main__":
    print(config)
