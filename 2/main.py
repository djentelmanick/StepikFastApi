from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel


# from typing import List


app = FastAPI()
# application = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World! 2025"}


@app.get("/easy")
async def easy():
    return {"message": "Добро пожаловать в моё приложение FastAPI!"}


@app.get("/page")
async def page():
    return FileResponse("public/index.html")


@app.get("/page_test", response_class=FileResponse)
async def page_test():
    return "public/index.html"


@app.get("/calculate/{expression}")
async def calculate(expression: str):
    try:
        eval(expression)
        return {"result": eval(expression)}
    except Exception:
        return {"result": "Incorrect expression"}


class Num(BaseModel):
    num: int


# @app.post("/calculate")
# async def calculate(nums: List[Num]):
#     return {"result": sum([number.num for number in nums])}
# fetch('http://127.0.0.1:8000/calculate',
# {method: 'POST',
# headers: {'Content-Type': 'application/json'},
# body: JSON.stringify([{'num': 5}, {'num': 2}, {'num': -1}])})


# @app.post("/calculate")
# async def calculate(nums: List[int]):
#     return {"result": sum(nums)}
# curl -X POST "http://localhost:8000/calculate" -H "Content-Type: application/json" -d "[5, 10, 11]"


class Summation(BaseModel):
    number1: int = 0
    number2: int = 0


@app.post("/calculate")
async def post_calculate(nums: Summation):
    return {"result": nums.number1 + nums.number2}
