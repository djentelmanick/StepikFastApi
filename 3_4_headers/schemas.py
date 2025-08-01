from babel import Locale
from babel.core import UnknownLocaleError
from pydantic import BaseModel, field_validator


class CommonHeaders(BaseModel):
    user_agent: str
    accept_language: str

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
