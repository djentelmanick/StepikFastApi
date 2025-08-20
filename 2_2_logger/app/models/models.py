from datetime import datetime

from pydantic import BaseModel


# Создаём модель данных, которая обычно располагается в файле models.py
class User(BaseModel):
    id: int
    name: str = "John Doe"
    signup_ts: datetime | None = None
    friends: list[int] = []


external_data = {
    "id": "123",
    "signup_ts": "2017-06-01 12:22",
    "friends": [1, "2", b"3"],
}

user = User(**external_data)
# print(user)
# print(user.id)


def check_user_id(user_id: int):
    return user_id


print(check_user_id(2))
