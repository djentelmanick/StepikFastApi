from babel import Locale
from babel.core import UnknownLocaleError
from fastapi import HTTPException, status
from pydantic import BaseModel, field_validator


MINIMUM_APP_VERSION = "1.100.500"


class CommonHeaders(BaseModel):
    user_agent: str
    accept_language: str
    x_current_version: str

    @field_validator("accept_language")
    def validate_accept_language(cls, v):
        try:
            for lang in v.split(","):
                lang_code = lang.split(";")[0].strip()
                if lang_code:
                    Locale.parse(lang_code, sep="-")
        except UnknownLocaleError:
            raise ValueError(f"Invalid language tag: {lang_code}")
        except Exception as e:
            raise ValueError(f"Invalid Accept-Language format: {str(e)}")
        return v

    @field_validator("x_current_version")
    def validate_x_current_version(cls, v):
        for min_version, input_version in zip(MINIMUM_APP_VERSION.split("."), v.split(".")):
            if int(input_version) > int(min_version):
                return v
            if int(min_version) > int(input_version):
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=f"Minimum app version is {MINIMUM_APP_VERSION}. Your version: {v}",
                )
        return v
