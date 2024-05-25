from typing import Generator
from sqlalchemy.orm import Session
from app.db.session import SessionLocal

def get_db() -> Generator[Session, None, None]:
    """
    Dependency that provides a database session.
    Yields a new session and ensures it is closed after the request is finished.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
