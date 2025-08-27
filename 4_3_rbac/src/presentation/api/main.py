from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi_limiter import FastAPILimiter
from redis import asyncio as aioredis
from src.config import settings
from src.presentation.api.routers import list_routers


@asynccontextmanager
async def lifespan(_: FastAPI):
    redis_connection = aioredis.from_url("redis://localhost:6379", encoding="utf8")
    await FastAPILimiter.init(redis_connection)
    yield
    await FastAPILimiter.close()


app = FastAPI(lifespan=lifespan)

for router in list_routers:
    app.include_router(router, prefix=settings.app.path_prefix)
