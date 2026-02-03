from fastapi.testclient import TestClient

from app.main import create_app


def test_root_ok():
    client = TestClient(create_app())
    r = client.get("/")
    assert r.status_code == 200
    body = r.json()
    assert body["ok"] is True
    assert body["name"]
    assert body["docs"] == "/docs"
    assert body["openapi"] == "/openapi.json"


def test_health_ok():
    client = TestClient(create_app())
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"ok": True}


def test_healthz_has_fields():
    client = TestClient(create_app())
    r = client.get("/api/healthz")
    assert r.status_code == 200
    body = r.json()
    assert body["ok"] is True
    assert "env" in body
    assert "ts" in body


def test_version_ok():
    client = TestClient(create_app())
    r = client.get("/api/version")
    assert r.status_code == 200
    body = r.json()
    assert body["name"]
    assert body["version"]
