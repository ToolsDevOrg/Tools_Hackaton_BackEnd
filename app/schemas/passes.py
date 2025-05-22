from pydantic import BaseModel
from datetime import date, time

from app.models.enums import PassTypeEnum

class PassCreate(BaseModel):
    title: str
    start_date: date
    location: str
    policy_area: str
    organizer: str
    latitude: float
    longitude: float
    participants: int
    active_from: date
    work_time_from: time
    pass_type: PassTypeEnum