from pydantic import BaseModel, EmailStr, Field


class SignUpUser(BaseModel):
    email: EmailStr
    username: str = Field(min_length=4, max_length=50)
    password: str = Field(min_length=10, max_length=50)
    confirm_password: str = Field(min_length=10, max_length=50)
