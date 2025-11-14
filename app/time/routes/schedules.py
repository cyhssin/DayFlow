from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from typing import List

from shared.database.session import get_db
from app.time.schemas.schedule import ScheduleCreate, ScheduleResponse  # ✅ Updated
from app.time.crud.schedule import (  # ✅ Updated
    create_schedule, get_schedules_by_date, get_schedules_by_date_range, delete_schedule
)

router = APIRouter(prefix="/schedules", tags=["schedules"])

@router.post("/", response_model=ScheduleResponse)
def create_new_schedule(schedule: ScheduleCreate, db: Session = Depends(get_db)):
    return create_schedule(db, schedule)

@router.get("/date/{target_date}", response_model=List[ScheduleResponse])
def get_schedules_for_date(target_date: date, db: Session = Depends(get_db)):
    return get_schedules_by_date(db, target_date)

@router.get("/range/{start_date}/{end_date}", response_model=List[ScheduleResponse])
def get_schedules_in_range(start_date: date, end_date: date, db: Session = Depends(get_db)):
    if start_date > end_date:
        raise HTTPException(status_code=400, detail="Start date must be before end date")
    return get_schedules_by_date_range(db, start_date, end_date)

@router.delete("/{schedule_id}")
def remove_schedule(schedule_id: int, db: Session = Depends(get_db)):
    delete_schedule(db, schedule_id)
    return {"message": "Schedule deleted"}