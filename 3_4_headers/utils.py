from typing import Annotated

from fastapi import Header, HTTPException
from schemas import CommonHeaders


async def get_common_headers(
    user_agent: Annotated[str, Header()],
    accept_language: Annotated[str, Header()],
    x_current_version: str =  Header(
        ...,
        description="Текущая версия клиента в формате X.Y.Z",
        pattern=r"^\d+\.\d+\.\d+$",
        examples=["1.2.3"]
    )
) -> CommonHeaders:
    try:
        return CommonHeaders(user_agent=user_agent, accept_language=accept_language, x_current_version=x_current_version)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
