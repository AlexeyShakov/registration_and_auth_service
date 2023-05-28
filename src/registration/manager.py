from enums import RoleChoices
import bcrypt
from sqlalchemy.ext.asyncio import AsyncSession
from database_conn import Base
from models import User
from registration.utils import get_obj


class UserManager:
    async def create(self, model: Base, session: AsyncSession, user_obj: dict):
        password = user_obj["password"]
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        user_obj["password"] = hashed_password.decode()

        obj = model(**user_obj)
        session.add(obj)
        await session.commit()
        return obj

    async def get_user_by_username(self, username: str, session: AsyncSession) -> Base | bool:
        if user_obj := await get_obj(model=User, identification_param=username, session=session):
            return user_obj
        return False

    async def validate_password(self, user_obj: User, password: str) -> bool:
        return bcrypt.hashpw(password.encode(), user_obj.password.encode()) == user_obj.password.encode()

    async def validate_token(self, token: str) -> bool | int:
        pass

