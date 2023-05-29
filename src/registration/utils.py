from fastapi import Depends

from database_conn import Base, get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


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