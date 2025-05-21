from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession


class BaseDAO:
    model = None

    @classmethod
    async def find_one_or_none(cls, db: AsyncSession, **filter_by):
        query = select(cls.model).filter_by(**filter_by)
        result = await db.execute(query)
        return result.scalars().one_or_none()

    @classmethod
    async def find_all(cls, db: AsyncSession, **filter_by):
        query = select(cls.model).filter_by(**filter_by)
        result = await db.execute(query)
        return result.scalars().all()

    @classmethod
    async def insert_by_data(cls, db: AsyncSession, entity_data: dict):
        query = insert(cls.model).values(entity_data).returning(cls.model)
        result = await db.execute(query)
        await db.commit()
        return result.scalars().one()

    @classmethod
    async def delete_by_filter(cls, db: AsyncSession, **filter_by):
        query = delete(cls.model).filter_by(**filter_by).returning(cls.model)
        result = await db.execute(query)
        await db.commit()
        return result.scalars().one()

    @classmethod
    async def update_by_filter(cls, db: AsyncSession, update_data: dict, *filter, **filter_by):
        query = update(cls.model).filter(*filter).filter_by(**filter_by).values(update_data).returning(cls.model)
        result = await db.execute(query)
        await db.commit()
        return result.scalars().one()
