from datetime import datetime

from fastapi import Depends, FastAPI, Response
from schemas import CommonHeaders
from utils import get_common_headers


app = FastAPI()


@app.get("/headers", tags=["headers"])
async def get_headers(headers: CommonHeaders = Depends(get_common_headers)):
    return headers


@app.get("/info", tags=["info"])
async def read_info(response: Response, headers: CommonHeaders = Depends(get_common_headers)):
    response.headers["X-Server-Time"] = datetime.now().isoformat()
    return {
        "message": "Добро пожаловать! Ваши заголовки успешно обработаны.",
        "headers": headers,
    }
