from fastapi import Depends

from database_conn import Base, get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


async def get_obj(model: Base, identification_param: str | int, session: AsyncSession) -> Base | bool:
    try:
        query = select(model).where(model.username == identification_param)
    except:
        query = select(model).where(model.id == identification_param)
    result = await session.execute(query)
    obj = result.scalars().first()
    if not obj:
        return False
    return obj