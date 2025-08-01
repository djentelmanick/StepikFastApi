from typing import Annotated

from fastapi import Header, HTTPException
from schemas import CommonHeaders


async def get_common_headers(
    user_agent: Annotated[str, Header()],
    accept_language: Annotated[str, Header()],
) -> CommonHeaders:
    try:
        return CommonHeaders(user_agent=user_agent, accept_language=accept_language)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
