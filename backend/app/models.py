from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class Agent(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    handle: str = Field(index=True, min_length=1, max_length=64)
    display_name: Optional[str] = Field(default=None, max_length=128)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Post(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    agent_id: int = Field(index=True)
    platform: str = Field(default="moltx", max_length=32)
    url: Optional[str] = Field(default=None, max_length=512)
    content: str = Field(min_length=1)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class MetricEvent(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    agent_id: int = Field(index=True)
    kind: str = Field(index=True, max_length=64)  # e.g. impression|like|reply|share
    value: int = Field(default=1)
    created_at: datetime = Field(default_factory=datetime.utcnow)
