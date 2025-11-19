from fastapi import FastAPI
from app.todo.routes.todos import router as todos_router

from shared.database.session import create_tables

app = FastAPI(title="Todo Service")

app.include_router(todos_router)

@app.get("/")
def read_root():
    return {"service": "Todo Service", "status": "running"}