from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Query
from sqlalchemy import Column, DateTime, func, String
from contextlib import contextmanager, asynccontextmanager
from typing import AsyncGenerator
import logging
from app.conf.config import DBSettings

Base = declarative_base()


def get_db():
    db_url = DBSettings.SQLALCHEMY_DATABASE_URL
    logging.info("db_url %s", db_url)
    engine = create_async_engine(
        db_url, pool_size=10,
        max_overflow=2,
        pool_recycle=300,
        pool_pre_ping=True,
        pool_use_lifo=True,
        echo=False
    )
    logging.info("created sqlalchemy engine")
    return engine


class SoftDeleteScopeQuery(Query):
    """
    Custom query class to scope the default query to not show/reviews soft delete records
    """

    def __new__(cls, *args, **kwargs):
        if args and args[0] and hasattr(args[0][0],
                                        "deleted_timestamp"):
            return Query(*args, **kwargs).filter_by(deleted_at=None)

        return object.__new__(cls)


async_session = sessionmaker(autocommit=False, autoflush=False,
                             # expire_on_commit=False,
                             bind=get_db(), class_=AsyncSession,
                             query_cls=SoftDeleteScopeQuery)


@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Provide a transactional scope around a series of operations."""
    async with async_session() as session:
        async with session.begin():
            try:
                yield session
            finally:
                await session.close()


class Timestampedtable:
    """
    Template table structure for the application
    """

    created_timestamp = Column(DateTime, default=func.now(),
                               nullable=False)
    modified_timestamp = Column(DateTime, default=func.now(),
                                onupdate=func.now(), nullable=False)
    deleted_timestamp = Column(DateTime, default=func.now(),
                               onupdate=func.now(), nullable=False)
    created_by_userid = Column(String(50))
    modified_by_userid = Column(String(50))
