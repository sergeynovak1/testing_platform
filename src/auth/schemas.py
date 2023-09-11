from datetime import datetime

from pydantic import BaseModel, EmailStr


# class UserCreate(BaseModel):
#     email: EmailStr
#     password: str


class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str
    first_name: str
    last_name: str = None
    date_of_birth: datetime = datetime.utcnow()
    phone_number: str


class UserOut(BaseModel):
    username: str
    first_name: str
    last_name: str
    is_active: bool