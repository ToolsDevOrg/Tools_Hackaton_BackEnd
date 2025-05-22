import uuid

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.users import RefreshSession
from app.repositories.base import SQLAlchemyRepository


class RefreshSessionRepository(SQLAlchemyRepository):
    model = RefreshSession

    def __init__(self, session: AsyncSession):
        self.session = session

    async def update_session(self, refresh_session_id: uuid.UUID, refresh_token: uuid.UUID, expires_in: int) -> None:
        """Обновить сессию"""
        query = (
            update(RefreshSession)
            .where(RefreshSession.id == refresh_session_id)
            .values(refresh_token=refresh_token, expires_in=expires_in)
        )
        await self.session.execute(query)
