"""
Sets up postgresql database connection pool.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker, Session
import settings

engine = create_engine(
    f"postgresql+psycopg2://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}",
    future=True,
    pool_pre_ping=True,
    pool_size=5,
    pool_timeout=10,
)


session_maker = sessionmaker(engine)


def get_db() -> Session:
    return session_maker()
