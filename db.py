import os
from urllib.parse import quote_plus

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


def _database_url() -> str:
    """Prefer DATABASE_URL; otherwise build a MySQL URL from MYSQL_* env vars."""
    explicit = os.getenv("DATABASE_URL")
    if explicit:
        return explicit

    user = os.getenv("MYSQL_USER", "root")
    password = os.getenv("MYSQL_PASSWORD", "")
    host = os.getenv("MYSQL_HOST", "localhost")
    port = os.getenv("MYSQL_PORT", "3306")
    database = os.getenv("MYSQL_DATABASE", "")

    user_enc = quote_plus(user)
    if password:
        auth = f"{user_enc}:{quote_plus(password)}"
    else:
        auth = user_enc

    return f"mysql+pymysql://{auth}@{host}:{port}/{database}"


DATABASE_URL = _database_url()

connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
