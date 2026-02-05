from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import create_app


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
