from fastapi import FastAPI
from app.time.routes import schedules  # ✅ Updated

app = FastAPI(title="Timely - Time Tracking Service")

app.include_router(schedules.router)  # ✅ This should work now

@app.get("/")
def read_root():
    return {"message": "Welcome to Timely - Schedule & Track Your Time"}