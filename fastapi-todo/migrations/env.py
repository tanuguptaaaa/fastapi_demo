from logging.config import fileConfig

from sqlalchemy import engine_from_config
from alembic import context
from sqlalchemy import engine_from_config, pool
from logging.config import fileConfig
from app.models import Base  # Import your SQLAlchemy Base or MetaData object

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
fileConfig(config.config_file_name)

# Import the metadata object from your models
target_metadata = Base.metadata  # Ensure you are using the correct metadata object

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

run_migrations_online()
