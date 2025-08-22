from src.api.crypt_context import pwd_context
from src.api.schemas import UserInDB


fake_users_db = [
    UserInDB(username="user1", hashed_password=pwd_context.hash("pass1")),
    UserInDB(username="user2", hashed_password=pwd_context.hash("pass2")),
]


if __name__ == "__main__":
    print(fake_users_db)
