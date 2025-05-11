from fastapi import APIRouter
from src.api.db.users import db_users
from src.api.schemas.user import User


users = APIRouter()


@users.get("/users")
async def get_users():
    response = dict()
    for user in db_users:
        response[user.id] = {"name": user.name, "age": user.age}
    return response


@users.get("/users/{id_user}")
async def get_user(id_user: int):
    for user in db_users:
        if user.id == id_user:
            return f"По id {id_user} нашелся пользователь {user.name} ({user.age} лет)!"
    return f"Пользователя с id {id_user} нет"


@users.post("/users")
async def add_user(user: User):
    for user_dp in db_users:
        if user_dp.id == user.id:
            return "Пользователь с таким id уже существует!"
    db_users.append(user)
    # return f"Пользвователь {user.name} с id {user.id} успешно добавлен!"
    is_adult = True if user.age >= 18 else False
    return {"id": user.id, "name": user.name, "age": user.age, "is_adult": is_adult}


@users.delete("/users/{id_user}")
async def delete_user(id_user: int):
    for user in db_users:
        if user.id == id_user:
            response = f"Пользователь {user.name} с id {id_user} успешно удален!"
            db_users.remove(user)
            return response
    return f"Пользователя с id {id_user} нет"
