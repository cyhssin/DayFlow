from sqlalchemy import Column, Integer, String, Float, Date, DateTime, Boolean
from shared.database.base import Base
from datetime import datetime

class Schedule(Base):
    __tablename__ = "schedules"
    id = Column(Integer, primary_key=True, index=True)
    activity = Column(String, index=True)
    hours = Column(Float)
    date = Column(Date)
    planned = Column(Boolean, default=True)  # True = scheduled, False = log
    created_at = Column(DateTime, default=datetime.utcnow)