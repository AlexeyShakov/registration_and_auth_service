from typing import Optional
from pydantic import BaseModel

from config import SECRET


class UserSchemaBase(BaseModel):
    username: str
    first_name: str
    last_name: str
    surname: Optional[str]
    phone: str
    email: str
    has_helpdesk_permission: bool


class UserSchemaCreate(UserSchemaBase):
    password: str

class UserSchemaReturn(UserSchemaBase):
    id: int

    class Config:
        orm_mode = True


class LoginSchema(BaseModel):
    username: str
    password: str


class Settings(BaseModel):
    authjwt_secret_key: str = SECRET


class TokenSchema(BaseModel):
    access: str
