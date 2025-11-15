from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from shared.database.session import get_db
from app.todo.schemas.todo import TodoCreate, TodoUpdate, TodoResponse

router = APIRouter(prefix="/todos", tags=["todos"])

@router.post("/", response_model=TodoResponse)
def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    from app.todo.crud.todo import create_todo as crud_create_todo
    return crud_create_todo(db, todo)

@router.get("/{todo_id}", response_model=TodoResponse)
def get_todo(todo_id: int, db: Session = Depends(get_db)):
    from app.todo.crud.todo import get_todo as crud_get_todo
    db_todo = crud_get_todo(db, todo_id)
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo

@router.get("/", response_model=List[TodoResponse])
def get_todos(
    skip: int = 0, 
    limit: int = 100, 
    completed: bool = None, 
    db: Session = Depends(get_db)
):
    from app.todo.crud.todo import get_todos as crud_get_todos
    return crud_get_todos(db, skip=skip, limit=limit, completed=completed)

@router.put("/{todo_id}", response_model=TodoResponse)
def update_todo(todo_id: int, todo_update: TodoUpdate, db: Session = Depends(get_db)):
    from app.todo.crud.todo import update_todo as crud_update_todo
    db_todo = crud_update_todo(db, todo_id, todo_update)
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo

@router.delete("/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    from app.todo.crud.todo import delete_todo as crud_delete_todo
    success = crud_delete_todo(db, todo_id)
    if not success:
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"message": "Todo deleted successfully"}