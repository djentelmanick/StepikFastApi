from fastapi import FastAPI
from app.logger import logger
from app.config import load_config

app = FastAPI()
# config = load_config("./.env")
config = load_config()


@app.get("/db")
def get_db_info():
    logger.info(f"Connecting to database: {config.db.database_url}")
    return {"database_url": config.db.database_url}
