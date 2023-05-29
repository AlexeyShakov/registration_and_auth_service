import bcrypt
from sqlalchemy.ext.asyncio import AsyncSession
from database_conn import Base
from models import User
from registration.utils import get_obj
import jwt
from config import SECRET, JWT_ALGORITHM
from fastapi import HTTPException


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
        if user_obj := await get_obj(model=User, session=session, username=username):
            return user_obj
        return False

    async def validate_password(self, user_obj: User, password: str) -> bool:
        return bcrypt.hashpw(password.encode(), user_obj.password.encode()) == user_obj.password.encode()

    async def decode_token(self, token: str) -> dict:
        try:
            decoded_token = jwt.decode(token, SECRET, algorithms=JWT_ALGORITHM)
        except jwt.exceptions.InvalidSignatureError:
            raise HTTPException(status_code=401, detail="Invalid signature")
        except jwt.exceptions.InvalidAlgorithmError:
            raise HTTPException(status_code=401, detail="Invalid algorithm")
        except jwt.exceptions.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Signature has expired")
        except Exception:
            raise HTTPException(status_code=401, detail="Problems with the token")
        return decoded_token
