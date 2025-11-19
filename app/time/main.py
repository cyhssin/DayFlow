from fastapi import FastAPI
from app.time.routes import schedules

from shared.database.session import create_tables

app = FastAPI(title="Timely - Time Tracking Service")

app.include_router(schedules.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Timely - Schedule & Track Your Time"}