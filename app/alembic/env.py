import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config  # type: ignore
from sqlalchemy import pool

from pydantic import BaseModel, PostgresDsn, validator, ValidationError

from alembic import context  # type: ignore

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = None

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


class Database(BaseModel):
    uri: PostgresDsn

    @validator("uri")
    def check_db_name(cls, v):
        assert v.path and len(v.path) > 1, "database must be provided"
        return v


def get_url():
    try:
        return f"{Database(uri=os.environ['APP_DATABASE_URI']).uri}"
    except KeyError or ValidationError:
        user = os.getenv("POSTGRES_USER", "postgres")
        password = os.getenv("POSTGRES_PASSWORD", "")
        server = os.getenv("POSTGRES_SERVER", "db")
        db = os.getenv("POSTGRES_DB", "app")
        return f"postgresql://{user}:{password}@{server}/{db}"


def get_schema():
    return os.environ.get("POSTGRES_SCHEMA", "public")


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = get_url()
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    target_schema = get_schema()
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            version_table_schema=target_schema,
        )
        connection.execute(f"CREATE SCHEMA IF NOT EXISTS {target_schema}")
        connection.execute(f"SET SEARCH_PATH TO {target_schema}")

        connection.dialect.default_schema_name = target_schema

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
