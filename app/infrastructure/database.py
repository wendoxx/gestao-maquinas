from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.infrastructure.config import settings

# Create an engine to access database
engine = create_engine(settings.database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine,
                            autoflush=False,
                            expire_on_commit=False)


class Base(DeclarativeBase):
    pass

# Create and close a session
def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
