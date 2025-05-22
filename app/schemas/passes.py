import uuid
from datetime import date, datetime, time

from pydantic import BaseModel, model_validator

from app.exceptions.passes.exceptions import RequiredCarNumberExc
from app.models.enums import PassStatusEnum, PassTypeEnum


class SPassCreate(BaseModel):
    title: str
    start_date: date
    location: str
    policy_area: str
    organizer: str
    latitude: float
    longitude: float
    participants: int
    active_from: date
    car_number: str | None
    work_time_from: time
    pass_type: PassTypeEnum

    @model_validator(mode="before")
    @classmethod
    def check_car_number_for_car_type(cls, values: dict):
        pass_type = values.get("pass_type")
        car_number = values.get("car_number")

        if pass_type == PassTypeEnum.CAR and not car_number:
            raise RequiredCarNumberExc

        return values


class SPassCurrent(BaseModel):
    id: uuid.UUID
    start_date: date
    title: str
    longitude: float
    organizer: str
    pass_type: PassTypeEnum
    location: str
    created_at: datetime
    latitude: float
    policy_area: str
    participants: int
    car_number: str | None
    status: PassStatusEnum
