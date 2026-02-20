from __future__ import annotations

from collections.abc import Generator

from sqlmodel import Session, SQLModel, create_engine

from .settings import get_settings


def get_engine():
    settings = get_settings()
    # sqlite is the default for local/dev; swap via DATABASE_URL in prod
    return create_engine(settings.DATABASE_URL, echo=False)


def init_db() -> None:
    # Ensure model tables are registered on SQLModel.metadata
    from . import models  # noqa: F401

    engine = get_engine()
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    engine = get_engine()
    with Session(engine) as session:
        yield session
