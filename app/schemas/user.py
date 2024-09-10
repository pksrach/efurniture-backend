from pydantic import BaseModel, EmailStr, Field


class RegisterUserRequest(BaseModel):
    username: str = Field(default="user")
    password: str = Field(default="User@123")
    email: EmailStr = Field(default="user@example.com")


class EmailRequest(BaseModel):
    email: EmailStr


class ResetRequest(BaseModel):
    token: str
    email: EmailStr
    password: str
