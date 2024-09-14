from pydantic import EmailStr, BaseModel, Field


class LoginRequest(BaseModel):
    username: str = Field(default="user")
    password: str = Field(default="User@123")
    email: EmailStr = Field(default="user@example.com")


class VerifyPasswordRequest(BaseModel):
    code: str = Field(default="1234")
    token: str = Field(default="token")


class ResetNewPasswordRequest(BaseModel):
    password: str = Field(default="User@123")
    user_id: str = Field(default="user_id")