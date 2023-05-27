from typing import Optional

from fastapi_users import schemas
from pydantic import EmailStr

from enums import RoleChoices


class UserRead(schemas.BaseUser[int]):
    id: int
    username: str
    first_name: str
    last_name: str
    patronymic: Optional[str]
    phone_number: str
    role: RoleChoices
    ####
    email: EmailStr
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False


class UserCreate(schemas.BaseUserCreate):
    username: str
    first_name: str
    last_name: str
    patronymic: Optional[str]
    phone_number: str
    role: RoleChoices = RoleChoices.USER
    ####
    email: EmailStr
    password: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False

# class UserUpdate(schemas.BaseUserUpdate):
#     pass