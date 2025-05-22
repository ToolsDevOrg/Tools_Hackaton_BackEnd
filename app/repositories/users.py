import uuid

from sqlalchemy import update
from app.models.users import RefreshSession, User
from app.repositories.base import SQLAlchemyRepository
from sqlalchemy.ext.asyncio import AsyncSession

class UsersRepository(SQLAlchemyRepository):
    model = User

    def __init__(self, session: AsyncSession):
        self.session = session