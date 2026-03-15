from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pathlib import Path

DATABASE_URL = f"sqlite:///{Path('app.db').resolve()}"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocsal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def get_db():
    db = SessionLocsal()
    try:
        yield db
    finally:
        db.close()