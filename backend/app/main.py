from __future__ import annotations

from contextlib import asynccontextmanager
from datetime import datetime, timezone

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api import router as api_router
from .db import init_db
from .settings import get_settings


def create_app() -> FastAPI:
    settings = get_settings()

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        # Ensure local/dev sqlite schema exists. In prod we may use migrations.
        init_db()
        yield

    app = FastAPI(title="MoltX Warlords API", version="0.1.0", lifespan=lifespan)

    if settings.cors_origins:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.cors_origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    @app.get("/")
    def root():
        return {
            "name": "moltx-warlords-backend",
            "ok": True,
            "docs": "/docs",
            "openapi": "/openapi.json",
        }

    @app.get("/health")
    def health():
        # keep this endpoint stable for infra checks
        return {"ok": True}

    @app.get("/healthz")
    @app.get("/api/healthz")
    def healthz():
        return {
            "ok": True,
            "env": settings.ENV,
            "ts": datetime.now(timezone.utc).isoformat(),
        }

    @app.get("/api/version")
    def version():
        return {
            "name": "moltx-warlords-backend",
            "version": app.version,
            "sha": settings.GIT_SHA or None,
        }

    app.include_router(api_router)

    return app


app = create_app()
