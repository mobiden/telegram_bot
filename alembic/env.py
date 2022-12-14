from logging.config import fileConfig

import yaml
from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
from app.store.database.sa_db import sa_db
from app.web.config import DatabaseConfig

with open('config.yml') as cf:
    cfg = yaml.safe_load(cf)
    database = cfg['database']['db']
    app_config = DatabaseConfig(**cfg.get(database, {}))


def set_sqlalchemy_url(db_name:str, username:str, password:str, host:str, port:str, db: str):

    print(f"{db_name}://{username}:{password}@{host}:{port}/{db}")
    config.set_main_option('sqlalchemy.url', f"{db_name}://{username}:{password}@{host}:{port}/{db}")


config = context.config


# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = sa_db

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    set_sqlalchemy_url(app_config.db_name, app_config.user, app_config.password,  # added
                       app_config.host, app_config.port, app_config.database)
    url = config.get_main_option("sqlalchemy.url")
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
    set_sqlalchemy_url(app_config.db_name, app_config.user, app_config.password,  # added
                       app_config.host, app_config.port, app_config.database)
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
