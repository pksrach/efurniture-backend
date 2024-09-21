from pydantic import BaseModel, EmailStr, Field


class RegisterUserRequest(BaseModel):
    username: str
    password: str
    email: EmailStr


class EmailRequest(BaseModel):
    email: EmailStr


class ResetRequest(BaseModel):
    token: str
    email: EmailStr
    password: str
