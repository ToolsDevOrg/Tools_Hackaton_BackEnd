from app.config.database import async_session_maker
from app.repositories.passes import PassesRepository
from app.repositories.refresh_session import RefreshSessionRepository
from app.repositories.users import (
    UsersRepository,
)


class UnitOfWork:
    def __init__(self):
        self.session_factory = async_session_maker

    async def __aenter__(self):
        self.session = self.session_factory()

        # Репозитории
        self.users = UsersRepository(self.session)
        self.refresh_session = RefreshSessionRepository(self.session)
        self.passes = PassesRepository(self.session)

    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
