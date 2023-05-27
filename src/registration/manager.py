from enums import RoleChoices
import bcrypt
from sqlalchemy.ext.asyncio import AsyncSession
from database_conn import Base

class UserManager:
    async def create(self, model: Base, session: AsyncSession, user_obj: dict):
        user_obj["role"] = RoleChoices.USER
        user_obj["is_superuser"] = False

        password = user_obj["password"]
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        user_obj["password"] = hashed_password.decode()

        obj = model(**user_obj)
        session.add(obj)
        await session.commit()
        return obj


