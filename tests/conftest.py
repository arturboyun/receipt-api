from typing import Generator, AsyncGenerator

import pytest
import pytest_asyncio
from faker import Faker
from fastapi.testclient import TestClient
from sqlalchemy import event, select, delete, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import Session, SessionTransaction

from app.api.v1.auth.utils import SecurityManager
from app.api.v1.payment.models import Payment
from app.api.v1.receipt.models import Product, Receipt
from app.api.v1.user.models import User
from app.config import settings
from app.dependencies import get_session

from app.main import app
from app.models import Base


@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="session")
def engine():
    engine = create_async_engine("postgresql+asyncpg://postgres:postgres@127.0.0.1:5432/postgres")
    yield engine
    engine.sync_engine.dispose()


@pytest.fixture()
def faker() -> Faker:
    faker = Faker()
    Faker.seed(0)
    return faker


async def init_db(session: AsyncSession):
    first_user_query = select(User).where(User.username == settings.FIRST_USER_USERNAME)
    first_user = await session.execute(first_user_query)
    first_user = first_user.scalar_one_or_none()
    if first_user:
        return
    user = User(
        username=settings.FIRST_USER_USERNAME,
        password=SecurityManager().get_password_hash(settings.FIRST_USER_PASSWORD),
        name=settings.FIRST_USER_NAME,
    )
    session.add(user)
    await session.commit()


@pytest_asyncio.fixture()
async def session() -> AsyncGenerator:
    # https://github.com/sqlalchemy/sqlalchemy/issues/5811#issuecomment-756269881
    async_engine = create_async_engine(str(settings.POSTGRES_URL))
    async with async_engine.connect() as conn:
        async_session_factory = async_sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=conn,
        )

        async with async_session_factory() as async_session:
            await init_db(async_session)

            yield async_session

            await async_session.execute(delete(Product))
            await async_session.execute(delete(Receipt))
            await async_session.execute(delete(Payment))
            # await async_session.execute(delete(User))
            await async_session.commit()
