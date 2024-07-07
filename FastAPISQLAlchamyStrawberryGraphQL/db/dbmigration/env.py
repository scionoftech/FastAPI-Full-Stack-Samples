from logging.config import fileConfig

from alembic import context
from sqlalchemy import create_engine
from app.conf.config import DBSettingsMigration

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use
alembic_config = context.config

# Interpret the config file for python logging.
# This line sets up loggers basically
fileConfig(alembic_config.config_file_name)

# add your model's Matadata object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = None


# other values from the config, defined by the needs of .env.py
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc


def get_db_url():
    db_url = DBSettingsMigration.SQLALCHEMY_DATABASE_URL
    return db_url


def run_migrations_offline():
    """
    Run migration in "offline" mode.

    This configuration the context with just a URL
    and not an engine, though an engine is acceptable
    here as well. By skipping the engine creation we dnt even need
    a DBAPI to available.
    """
    context.configure(url=get_db_url(),
                      target_metadata=target_metadata,
                      literal_binds=True,
                      dialect_opts={"paramstyle": "named"})

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """
    Run migrations in "online" mode.

    In this scenario we need to create an engine
    and associate a connection with the context
    """
    db_url = get_db_url()
    print(db_url)
    connectable = create_engine(db_url)

    with connectable.connect() as connection:
        context.configure(connection=connection,
                          target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
