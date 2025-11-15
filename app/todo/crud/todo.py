from sqlalchemy.orm import Session
from app.todo.models.todo import Todo
from app.todo.schemas.todo import TodoCreate, TodoUpdate

def create_todo(db: Session, todo: TodoCreate) -> Todo:
    db_todo = Todo(**todo.model_dump())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

def get_todo(db: Session, todo_id: int) -> Todo:
    return db.query(Todo).filter(Todo.id == todo_id).first()

def get_todos(db: Session, skip: int = 0, limit: int = 100, completed: bool = None) -> list[Todo]:
    query = db.query(Todo)
    if completed is not None:
        query = query.filter(Todo.completed == completed)
    return query.offset(skip).limit(limit).all()

def update_todo(db: Session, todo_id: int, todo_update: TodoUpdate) -> Todo:
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if db_todo:
        for field, value in todo_update.model_dump(exclude_unset=True).items():
            setattr(db_todo, field, value)
        db.commit()
        db.refresh(db_todo)
    return db_todo

def delete_todo(db: Session, todo_id: int) -> bool:
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if db_todo:
        db.delete(db_todo)
        db.commit()
        return True
    return False