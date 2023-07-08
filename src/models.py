from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Integer, Column, String, Boolean, Enum

from database_conn import Base
from enums import RoleChoices


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String(length=50), unique=True, index=True, nullable=False)
    first_name = Column(String(length=100), nullable=False)
    last_name = Column(String(length=100), nullable=False)
    surname = Column(String(length=100), nullable=True)
    phone = Column(String(length=50), nullable=True)
    role = Column(Enum(RoleChoices), nullable=False, default=RoleChoices.USER)
    email = Column(String(length=320), unique=True, index=True, nullable=False)
    password = Column(String(length=1024), nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
