from app.core.db import async_sessionmaker, engine


async def get_session():
    async with async_sessionmaker() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()
            await engine.dispose()
