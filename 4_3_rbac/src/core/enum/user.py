from enum import IntEnum, StrEnum


class UserRole(StrEnum):
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"


class RateLimitRole(IntEnum):
    ADMIN = 1000
    USER = 20
    GUEST = 5
