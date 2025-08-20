from typing import List

from src.api.schemas.user import User


test_user = User(id=1, name="First User", age="20")
test_user2 = User(id=2, name="Second User", age=34)

db_users: List[User] = [test_user, test_user2]
