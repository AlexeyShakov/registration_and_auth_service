from fastapi import Depends
from fastapi_jwt_auth import AuthJWT

from database_conn import Base, get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from config import JWT_ALGORITHM


async def get_obj(model: Base, session: AsyncSession, user_id: int = None, username: str = None) -> Base | bool:
    if user_id:
        query = select(model).where(model.id == user_id)
    else:
        query = select(model).where(model.username == username)
    result = await session.execute(query)
    obj = result.scalars().first()
    if not obj:
        return False
    return obj


async def create_tokens(username: str, additional_info: dict, token_creator: AuthJWT) -> dict:
    access_token = token_creator.create_access_token(subject=username, user_claims=additional_info, algorithm=JWT_ALGORITHM)
    refresh_token = token_creator.create_refresh_token(subject=username, user_claims=additional_info, algorithm=JWT_ALGORITHM)
    return {"access_token": access_token, "refresh_token": refresh_token}