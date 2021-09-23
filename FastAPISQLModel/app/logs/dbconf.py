from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from app.conf import DBSettings

engine = create_engine(
    DBSettings.SQLALCHEMY_DATABASE_URL, pool_size=10,
    max_overflow=2,
    pool_recycle=300,
    pool_pre_ping=True,
    pool_use_lifo=True
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


@contextmanager
def session_scope() -> SessionLocal:
    """Provide a transactional scope around a series of operations."""
    db = None
    try:
        db = SessionLocal()  # create session from SQLAlchemy sessionmaker
        yield db
    finally:
        db.close()
