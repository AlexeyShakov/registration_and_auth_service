from database import Base
from sqlalchemy.ext.asyncio import AsyncSession

async def create(model: Base, session: AsyncSession, data: dict) -> Base:
    obj = model(**data)
    session.add(obj)
    await session.commit()
    await session.refresh(obj)
    return obj