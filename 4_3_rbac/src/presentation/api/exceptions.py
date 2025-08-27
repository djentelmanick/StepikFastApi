from fastapi import HTTPException, status


class ApiError(HTTPException):
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail: str = "Unexpected Error Occured"
    headers: dict = {}

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail, headers=self.headers)


class ForbiddenError(ApiError):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "You don't have permission"


class ResourceNotFoundError(ApiError):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Resource not found"


class ResourceAlreadyExistsError(ApiError):
    status_code = status.HTTP_409_CONFLICT
    detail = "Resource already exists"


class UserNotFoundError(ApiError):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "User not found"
    # headers={"WWW-Authenticate": "Basic"}  не нужно из-за oauth формы


class AuthError(ApiError):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Authorization failed"
    # headers={"WWW-Authenticate": "Basic"}


class UnkownMethodError(ApiError):
    status_code = status.HTTP_405_METHOD_NOT_ALLOWED
    detail = "Method not allowed"
    headers = {"Allow": "GET, POST, PUT, DELETE"}


class TokenExpiredError(ApiError):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Token expired"
    headers = {"WWW-Authenticate": "Bearer", "X-Error-Redirect": "/login"}


class TokenInvalidError(ApiError):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Token invalid"
    headers = {"WWW-Authenticate": "Bearer"}
