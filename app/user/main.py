from fastapi import FastAPI
from app.user.routes.users import router as users_router

app = FastAPI(title="User Service")

# Tables are created in session.py now
app.include_router(users_router, prefix="/users", tags=["users"])

@app.get("/")
def read_root():
    return {"service": "User Service", "status": "running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}