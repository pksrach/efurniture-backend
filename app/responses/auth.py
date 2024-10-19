from pydantic import BaseModel

from app.responses.base import BaseResponse


class TokenData(BaseModel):
    access_token: str
    refresh_token: str
    expires_in: int


class TokenResponse(BaseResponse):
    data: TokenData
