from sqlalchemy.orm import Mapped, mapped_column
import uuid
from datetime import datetime, timezone
from sqlalchemy import TIMESTAMP, ForeignKey, Integer, String, UUID
from sqlalchemy.sql import func

from app.config.database import Base
from app.models.enums import UserRoleEnum, user_role_enum


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID, default=uuid.uuid4, primary_key=True)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=lambda: datetime.now(timezone.utc), server_default=func.now()
    )
    fio: Mapped[str | None] = mapped_column(String(255), nullable=True)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    password: Mapped[str] = mapped_column(String(255))
    jk_name: Mapped[str] = mapped_column(String(255), default="Москва, ул. Капитана Хакатонова, 2")
    phone: Mapped[str] = mapped_column(String(255))
    role: Mapped[UserRoleEnum] = mapped_column(user_role_enum)


class RefreshSession(Base):
    """Таблица для сессий пользователя"""

    __tablename__ = "refresh_session"

    id: Mapped[uuid.UUID] = mapped_column(UUID, default=uuid.uuid4, primary_key=True)
    refresh_token: Mapped[uuid.UUID] = mapped_column(UUID)
    expires_in: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=lambda: datetime.now(timezone.utc), server_default=func.now()
    )
    user_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("users.id", ondelete="CASCADE"))