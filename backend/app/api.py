from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select

from .db import get_session
from .models import Agent, MetricEvent, Post

router = APIRouter(prefix="/api")


@router.get("/db-check")
def db_check(session: Session = Depends(get_session)) -> dict:
    """Cheap DB connectivity check (read-only).

    Useful for readiness checks that want to verify DB is reachable in addition to /healthz.
    """

    # Run a trivial query to force a connection + ensure schema is initialized.
    session.exec(select(Agent.id).limit(1)).first()
    return {"ok": True}


@router.post("/agents", response_model=Agent)
def create_agent(agent: Agent, session: Session = Depends(get_session)) -> Agent:
    session.add(agent)
    session.commit()
    session.refresh(agent)
    return agent


@router.get("/agents", response_model=list[Agent])
def list_agents(
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    session: Session = Depends(get_session),
) -> list[Agent]:
    stmt = select(Agent).order_by(Agent.id.desc()).offset(offset).limit(limit)
    return list(session.exec(stmt).all())


@router.get("/agents/{agent_id}", response_model=Agent)
def get_agent(agent_id: int, session: Session = Depends(get_session)) -> Agent:
    agent = session.get(Agent, agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="agent not found")
    return agent


@router.post("/posts", response_model=Post)
def create_post(post: Post, session: Session = Depends(get_session)) -> Post:
    # minimal referential check (keeps sqlite schema simple for now)
    if not session.get(Agent, post.agent_id):
        raise HTTPException(status_code=400, detail="unknown agent_id")

    session.add(post)
    session.commit()
    session.refresh(post)
    return post


@router.get("/posts", response_model=list[Post])
def list_posts(
    agent_id: Optional[int] = None,
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    session: Session = Depends(get_session),
) -> list[Post]:
    stmt = select(Post).order_by(Post.id.desc())
    if agent_id is not None:
        stmt = stmt.where(Post.agent_id == agent_id)
    stmt = stmt.offset(offset).limit(limit)
    return list(session.exec(stmt).all())


@router.post("/events", response_model=MetricEvent)
def create_event(event: MetricEvent, session: Session = Depends(get_session)) -> MetricEvent:
    if not session.get(Agent, event.agent_id):
        raise HTTPException(status_code=400, detail="unknown agent_id")

    session.add(event)
    session.commit()
    session.refresh(event)
    return event


@router.get("/events", response_model=list[MetricEvent])
def list_events(
    agent_id: Optional[int] = None,
    kind: Optional[str] = None,
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    session: Session = Depends(get_session),
) -> list[MetricEvent]:
    stmt = select(MetricEvent).order_by(MetricEvent.id.desc())
    if agent_id is not None:
        stmt = stmt.where(MetricEvent.agent_id == agent_id)
    if kind is not None:
        stmt = stmt.where(MetricEvent.kind == kind)

    stmt = stmt.offset(offset).limit(limit)
    return list(session.exec(stmt).all())
