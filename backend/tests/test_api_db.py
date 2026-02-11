from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import create_app


def test_db_check(tmp_path, monkeypatch):
    db_path = tmp_path / "test.db"
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{db_path}")

    app = create_app()
    with TestClient(app) as client:
        r = client.get("/api/db-check")
        assert r.status_code == 200, r.text
        assert r.json()["ok"] is True


def test_readyz_includes_env_and_ts(tmp_path, monkeypatch):
    db_path = tmp_path / "test.db"
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{db_path}")

    app = create_app()
    with TestClient(app) as client:
        r = client.get("/api/readyz")
        assert r.status_code == 200, r.text
        body = r.json()
        assert body["ok"] is True
        assert body["env"]
        assert body["ts"]


def test_agents_posts_events_smoke(tmp_path, monkeypatch):
    db_path = tmp_path / "test.db"
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{db_path}")

    app = create_app()
    with TestClient(app) as client:
        # create agent
        r = client.post("/api/agents", json={"handle": "warlord-1", "display_name": "Warlord One"})
        assert r.status_code == 200, r.text
        agent = r.json()
        assert agent["id"]

        # create post
        r = client.post(
            "/api/posts",
            json={
                "agent_id": agent["id"],
                "platform": "moltx",
                "content": "hello attention economy",
                "url": "https://example.com/p/1",
            },
        )
        assert r.status_code == 200, r.text

        # create event
        r = client.post(
            "/api/events", json={"agent_id": agent["id"], "kind": "impression", "value": 5}
        )
        assert r.status_code == 200, r.text

        # list endpoints
        assert client.get("/api/agents").status_code == 200
        assert client.get("/api/posts").status_code == 200
        assert client.get("/api/events").status_code == 200


def test_unknown_agent_rejected(tmp_path, monkeypatch):
    db_path = tmp_path / "test.db"
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{db_path}")

    app = create_app()
    with TestClient(app) as client:
        r = client.post("/api/posts", json={"agent_id": 999, "content": "nope"})
        assert r.status_code == 400

        r = client.post("/api/events", json={"agent_id": 999, "kind": "like", "value": 1})
        assert r.status_code == 400


def test_list_endpoints_support_pagination(tmp_path, monkeypatch):
    db_path = tmp_path / "test.db"
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{db_path}")

    app = create_app()
    with TestClient(app) as client:
        # create a few agents
        for i in range(5):
            r = client.post(
                "/api/agents",
                json={"handle": f"warlord-{i}", "display_name": f"Warlord {i}"},
            )
            assert r.status_code == 200

        r = client.get("/api/agents?limit=2&offset=0")
        assert r.status_code == 200
        assert len(r.json()) == 2

        r = client.get("/api/agents?limit=2&offset=2")
        assert r.status_code == 200
        assert len(r.json()) == 2

        # guardrails
        assert client.get("/api/agents?limit=0").status_code == 422
        assert client.get("/api/agents?offset=-1").status_code == 422
