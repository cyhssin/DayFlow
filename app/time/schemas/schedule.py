from pydantic import BaseModel
from datetime import date, datetime

class ScheduleCreate(BaseModel):
    activity: str
    hours: float
    date: date

class ScheduleUpdate(BaseModel):
    activity: str
    hours: float

class ScheduleResponse(ScheduleCreate):
    id: int
    planned: bool
    created_at: datetime

    class Config:
        from_attributes = True