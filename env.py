import os
from alembic import context

config = context.config

database_url = os.getenv("DATABASE_URL")

if database_url:
    config.set_main_option("sqlalchemy.url", database_url)