from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from handlers.env_vars import EnvVars

engine = create_engine(EnvVars.DB_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
