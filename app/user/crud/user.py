from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext

from app.user.models.user import User
from app.user.schemas.user import UserCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_username(db: Session, username: str) -> User:
    """ Retrieve a user from the database by username """
    return db.query(User).filter(User.username == username).first()

def get_user_by_email(db: Session, email: str) -> User:
    """ Retrieve a user from the database by email """
    return db.query(User).filter(User.email == email).first()

def get_user_by_id(db: Session, user_id: int) -> User:
    """ Retrieve a user from the database by ID """
    return db.query(User).filter(User.id == user_id).first()

def create_user(db: Session, user: UserCreate) -> User:
    """ Create a new user in the database with a hashed password and verification token """
    hashed_password = pwd_context.hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
    )
    db.add(db_user)
    try:
        db.commit()
        db.refresh(db_user)
    except IntegrityError as err:
        db.rollback()
        raise ValueError("Username or email already exists") from err
    else:
        return db_user

def authenticate_user(db: Session, username: str, password: str) -> User:
    """ Authenticate a user by username and password """
    user = get_user_by_username(db, username)
    if not user:
        return None
    if not pwd_context.verify(password, user.hashed_password):
        return None
    if not user.is_active:
        return None
    return user

def delete_user(db: Session, user_id: int) -> bool:
    """ Delete a user from the database by ID """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return False
    db.delete(user)
    db.commit()
    return True

def deactivate_user(db: Session, user_id: int) -> User:
    """ Deactivate a user by ID """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None
    user.is_active = False
    db.commit()
    db.refresh(user)
    return user

def activate_user(db: Session, user_id: int) -> User:
    """ Activate a user by ID """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None
    user.is_active = True
    db.commit()
    db.refresh(user)
    return user
