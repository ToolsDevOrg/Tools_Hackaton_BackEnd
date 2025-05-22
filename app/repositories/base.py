import uuid

from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession


class SQLAlchemyRepository:
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, entity_id: uuid.UUID) -> model:
        """Получить сущность по ID."""
        query = select(self.model).where(self.model.id == entity_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_all(self) -> list[model]:
        """Получить список всех сущностей."""
        query = select(self.model)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def delete_by_filter(self, *filter, **filter_by) -> model:
        """Удалить сущность по фильтру"""
        query = delete(self.model).filter(*filter).filter_by(**filter_by).returning(self.model)
        result = await self.session.execute(query)
        return result.scalars().one()

    async def insert_by_data(self, entity_data: dict) -> model:
        """Добавить сущность"""
        query = insert(self.model).values(entity_data).returning(self.model)
        result = await self.session.execute(query)
        return result.scalars().one()

    async def update_by_filter(self, update_data: dict, *filter, **filter_by) -> model:
        """Обновить сущность по фильтру"""
        query = update(self.model).filter(*filter).filter_by(**filter_by).values(update_data).returning(self.model)
        result = await self.session.execute(query)
        return result.scalars().one()

    async def find_one_or_none(self, **filter_by) -> model:
        """Найти сущность по фильтру"""
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        return result.scalars().one_or_none()

    async def find_all(self, **filter_by) -> list[model]:
        """Найти все сущности, удовлетворяющие фильтру"""
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def find_all_by_filter(self, **filter_by) -> list[model]:
        """Найти все сущности, удовлетворяющие фильтру"""
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        return result.scalars().all()
