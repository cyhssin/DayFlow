from sqlalchemy.orm import Session
from typing import List
from datetime import date

from app.time.models.schedule import Schedule
from app.time.schemas.schedule import ScheduleCreate

def create_schedule(db: Session, schedule: ScheduleCreate) -> Schedule:
    db_schedule = Schedule(**schedule.model_dump())
    db.add(db_schedule)
    db.commit()
    db.refresh(db_schedule)
    return db_schedule

def get_schedules_by_date(db: Session, target_date: date) -> List[Schedule]:
    return db.query(Schedule).filter(Schedule.date == target_date).all()

def get_schedules_by_date_range(db: Session, start: date, end: date) -> List[Schedule]:
    return db.query(Schedule).filter(
        Schedule.date >= start,
        Schedule.date <= end
    ).order_by(Schedule.date).all()

def delete_schedule(db: Session, schedule_id: int):
    db.query(Schedule).filter(Schedule.id == schedule_id).delete()
    db.commit()