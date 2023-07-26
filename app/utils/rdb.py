from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.settings import app_settings

engine = create_engine(app_settings.DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_session() -> Session:
    return SessionLocal()
