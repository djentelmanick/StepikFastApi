import re

from pydantic import BaseModel, EmailStr, Field, field_validator


pattern = re.compile(
    r"\b(редис(ка|ку|кой|ке|ки|ок|кам|ками|ках)|бяк(а|и|е|у|ой|ою|ам|ами|ах)?|козявк(а|и|е|у|ой|ою|ам|ами|ах)?)\b",
    re.IGNORECASE,
)


class Contact(BaseModel):
    email: EmailStr
    phone: str | None = Field(None, min_length=7, max_length=15)

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, phone: str):
        if not phone.isdigit():
            raise ValueError("Номер телефона может содержать только цифры")
        return phone


class Feedback(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    message: str = Field(..., min_length=10, max_length=500)
    contact: Contact

    @field_validator("message")
    @classmethod
    def validate_message(cls, message: str):
        matches = re.findall(pattern, message)
        if matches:
            raise ValueError(f"Использование недопустимых слов: {[word[0] for word in matches]}")
        return message
