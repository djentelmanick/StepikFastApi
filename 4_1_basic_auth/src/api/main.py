from fastapi import Depends, FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from src.api.crypt_context import pwd_context
from src.api.db import fake_users_db
from src.api.schemas import User, UserInDB
from src.api.utils import auth_user, verify_docs_credentials
from src.core.config import config
from src.core.logger import LoggerConfig


LoggerConfig.setup()
logger = LoggerConfig.get_logger(__name__)

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)


@app.get("/login", tags=["User"])
async def auth(user: User = Depends(auth_user)):
    return "You got my secret, %s. Welcome!" % user.username


@app.post("/register", tags=["User"])
async def register(user: User):
    for user_db in fake_users_db:
        if user_db.username == user.username:
            return "User already exists"

    hashed_password = pwd_context.hash(user.password)
    fake_users_db.append(UserInDB(username=user.username, hashed_password=hashed_password))
    return "%s, you successfully registered!" % user.username


if config.mode == "DEV":
    logger.info("Running in development mode")

    @app.get("/docs", include_in_schema=False)
    async def get_documentation(user: User = Depends(verify_docs_credentials)):
        return get_swagger_ui_html(openapi_url="/openapi.json", title="Docs")

    @app.get("/openapi.json", include_in_schema=False)
    async def get_openapi_endpoint(user: User = Depends(verify_docs_credentials)):
        return get_openapi(title="API", version="1.0.0", routes=app.routes)

elif config.mode == "PROD":
    logger.info("Running in production mode")
