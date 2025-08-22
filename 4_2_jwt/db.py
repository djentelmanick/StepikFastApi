from secrets import compare_digest

from crypt_context import get_password_hash
from fastapi import HTTPException, status
from schemas import UserInDB


fake_users_db = [
    UserInDB(username="user1", hashed_password=get_password_hash("pass1")),
    UserInDB(username="user2", hashed_password=get_password_hash("pass2")),
]


def get_user_by_username(username: str) -> UserInDB | None:
    for user_db in fake_users_db:
        if compare_digest(user_db.username, username):
            return user_db
    return None


def add_user(user: UserInDB) -> None:
    if get_user_by_username(user.username):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists",
        )
    fake_users_db.append(user)


if __name__ == "__main__":
    print(fake_users_db)
