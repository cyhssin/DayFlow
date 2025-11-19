from sqlalchemy import Column, Integer, String, Float, Date, DateTime, Boolean, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from shared.database.base import Base

class Schedule(Base):
    __tablename__ = "schedules"
    
    id = Column(Integer, primary_key=True, index=True)
    activity = Column(String(255), nullable=False)
    hours = Column(Float, nullable=False)
    date = Column(Date, nullable=False)
    planned = Column(Boolean, default=True)
    owner_id = Column(Integer, ForeignKey("users.id", name="fk_schedule_owner_id"))
    created_at = Column(DateTime, server_default=func.now())
    
    owner = relationship("User", back_populates="schedules")