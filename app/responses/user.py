from datetime import datetime
from typing import Optional, Union
from uuid import UUID

from pydantic import EmailStr

from app.responses.base import BaseResponse


class UserDataResponse(BaseResponse):
    id: UUID | str
    username: str
    email: EmailStr
    is_active: bool
    role: str
    created_at: Optional[Union[str, datetime]] = None


class UserResponse(BaseResponse):
    data: UserDataResponse
