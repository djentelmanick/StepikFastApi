from api.endpoints import feedback
from fastapi import FastAPI


app = FastAPI()
app.include_router(feedback, tags=["feedback"])
