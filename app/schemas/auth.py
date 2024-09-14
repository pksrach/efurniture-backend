from pydantic import EmailStr, BaseModel, Field


class LoginRequest(BaseModel):
    username: str = Field(default="user")
    password: str = Field(default="User@123")
    email: EmailStr = Field(default="user@example.com")
