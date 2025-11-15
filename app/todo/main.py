from fastapi import FastAPI
from app.todo.routes.todos import router as todos_router
from shared.database.session import create_tables  # Import to ensure models are loaded

# Import models to register with Base
from app.todo.models import Todo# Replace 'Todo' with the actual model names you need

app = FastAPI(title="Todo Service")

# Create tables when app starts
create_tables()

app.include_router(todos_router)

@app.get("/")
def read_root():
    return {"service": "Todo Service", "status": "running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}