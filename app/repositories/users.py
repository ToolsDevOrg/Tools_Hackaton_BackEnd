import uuid

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.users import RefreshSession, User
from app.repositories.base import SQLAlchemyRepository


class UsersRepository(SQLAlchemyRepository):
    model = User

    def __init__(self, session: AsyncSession):
        self.session = session
