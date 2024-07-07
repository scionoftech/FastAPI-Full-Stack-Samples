import asyncio
from fastapi import FastAPI
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator
from contextlib import asynccontextmanager
from asgi_lifespan import LifespanManager
from httpx import AsyncClient
from db import Base, get_session


@pytest.fixture
def test_db_session():
    test_cases_engine = create_async_engine(
        "sqlite+aiosqlite:///:memory")
    async_test_cases_session = sessionmaker(bind=test_cases_engine,
                                            class_=AsyncSession,
                                            expire_on_commit=
                                            False, autocommit=False,
                                            autoflush=False)

    async def init_models():
        async with test_cases_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all())
            await conn.run_sync(Base.metadata.create_all())

    asyncio.run(init_models())
    return async_test_cases_session


@pytest.fixture
def app() -> FastAPI:
    from app.main import app

    test_cases_engine = create_async_engine(
        "sqlite+aiosqlite:///:memory")
    async_test_cases_session = sessionmaker(bind=test_cases_engine,
                                            class_=AsyncSession,
                                            expire_on_commit=
                                            False, autocommit=False,
                                            autoflush=False)

    async def init_models():
        async with test_cases_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all())
            await conn.run_sync(Base.metadata.create_all())

    asyncio.run(init_models())

    @asynccontextmanager
    async def override_get_session() -> AsyncGenerator[
        AsyncSession, None]:
        async with async_test_cases_session() as session:
            async with session.begin():
                try:
                    yield session
                finally:
                    await session.close()

    app.dependency_overrides[get_session] = override_get_session

    return app


@pytest.fixture
async def initialized_app(app: FastAPI) -> FastAPI:
    async with LifespanManager(app):
        yield app


@pytest.fixture
async def client(initialized_app: FastAPI) -> AsyncClient:
    async with AsyncClient(
            app=initialized_app,
            base_url="http://testserver",
            headers={"Content-Type": "application/json"}
    ) as client:
        yield client


@pytest.fixture
def authorized_client(client: AsyncClient, token: str,
                      authorization_prefix: str) -> AsyncClient:
    client.headers = {
        "Authorization": f"{authorization_prefix} {token}",
        **client.headers
    }
    return client


@pytest.fixture(autouse=True)
def set_secret_key_in_env(nonkeypatch):
    nonkeypatch.setenv("SECRET_KEY", "bla")


@pytest.fixture
def authorization_prefix() -> str:
    return "Brearer"


@pytest.fixture
def test_user():
    return {"userName": "test", "userpw": "test"}


@pytest.fixture
def token(test_user) -> str:
    from app.auth.token import access_token

    return access_token.create_access_token(test_user)
