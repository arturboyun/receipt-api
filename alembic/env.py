import asyncio
from logging.config import fileConfig
from pathlib import Path

from sqlalchemy import Connection
from sqlalchemy import pool
import importlib

from alembic import context
from sqlalchemy.ext.asyncio import async_engine_from_config

from app.config import settings

API_V1_PATH = settings.ROOT_PATH / "app" / "api" / "v1"


# import all models from app/api
# this is needed to autogenerate migrations
# for all models
def import_models_recursive(path: Path):
    if path.is_dir():
        for file in path.iterdir():
            if file.name == "models.py":
                module = file.relative_to(settings.ROOT_PATH).with_suffix("").as_posix().replace("/", ".")
                importlib.import_module(module)
            elif file.is_dir():
                import_models_recursive(file)


import_models_recursive(API_V1_PATH)

from app.models import Base


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata

target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

config.set_main_option("sqlalchemy.url", settings.POSTGRES_URL)


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = settings.postgres_path
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    engine = async_engine_from_config(
        context.config.get_section(context.config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    async with engine.connect() as connection:
        async with connection.begin():
            await connection.run_sync(do_run_migrations)
    await engine.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    asyncio.run(run_async_migrations_online())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
