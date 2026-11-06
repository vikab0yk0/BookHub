from pydantic import BaseModel, EmailStr, Field


class RegisterIn(BaseModel):

    username: str = Field(min_length=3, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8, max_length=100)


class LoginIn(BaseModel):

    email: EmailStr
    password: str


class TokenOut(BaseModel):
  
    access_token: str
    token_type: str = "bearer"