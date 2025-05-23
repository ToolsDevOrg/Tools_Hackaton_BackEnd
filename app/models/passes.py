import uuid
from datetime import date, datetime, timezone

from sqlalchemy import TIMESTAMP, UUID, Date, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.config.database import Base
from app.models.enums import PassStatusEnum, PassTypeEnum, pass_status_enum, pass_type_enum


class Passes(Base):

    __tablename__ = "passes"

    id: Mapped[uuid.UUID] = mapped_column(UUID, default=uuid.uuid4, primary_key=True)
    pass_number_ujin: Mapped[int] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=lambda: datetime.now(timezone.utc), server_default=func.now()
    )
    title: Mapped[str] = mapped_column(String(255))
    start_date: Mapped[date] = mapped_column(Date)
    location: Mapped[str] = mapped_column(String(255))
    latitude: Mapped[float] = mapped_column(Float)
    longitude: Mapped[float] = mapped_column(Float)
    policy_area: Mapped[str] = mapped_column(String(255))
    organizer: Mapped[str] = mapped_column(String(255))
    participants: Mapped[int] = mapped_column(Integer)
    pass_type: Mapped[PassTypeEnum] = mapped_column(pass_type_enum)
    car_number: Mapped[str | None] = mapped_column(String, nullable=True)
    status: Mapped[PassStatusEnum] = mapped_column(pass_status_enum, default=PassStatusEnum.UNCONFIRMED)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("users.id", ondelete="CASCADE"))
