from sqlmodel import Session, create_engine
from contextlib import contextmanager
from app.conf import DBSettings
from . import models

engine = create_engine(
    DBSettings.SQLALCHEMY_DATABASE_URL, pool_size=10,
    max_overflow=2,
    pool_recycle=300,
    pool_pre_ping=True,
    pool_use_lifo=True
)

models.SQLModel.metadata.create_all(engine)

@contextmanager
def session_scope() -> Session:
    """Provide a transactional scope around a series of operations."""
    db = None
    try:
        db = Session(autocommit=False, autoflush=False,
                     bind=engine)  # create session from SQLModel session
        yield db
    finally:
        db.close()


# class Hero(SQLModel, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)
#     name: str
#     secret_name: str
#     age: Optional[int] = None
