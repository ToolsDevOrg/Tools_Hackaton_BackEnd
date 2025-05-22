import uuid
from pydantic import BaseModel
from datetime import date, datetime, time

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
    work_time_from: time
    pass_type: PassTypeEnum
    
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
    status: PassStatusEnum
