from unittest.mock import patch

from fastapi.testclient import TestClient

from api.main import app, get_cors_origins


def test_login_response_contains_user_required_by_web_client():
    user = {"id": 7, "username": "tester", "is_active": True}

    with (
        patch("api.routers.auth.authenticate_user", return_value=user),
        patch("api.routers.auth.create_access_token", return_value="token"),
    ):
        response = TestClient(app).post(
            "/api/auth/login",
            json={"username": "tester", "password": "secret"},
        )

    assert response.status_code == 200
    assert response.json() == {
        "access_token": "token",
        "token_type": "bearer",
        "user": user,
    }


def test_environment_check_requires_authentication():
    response = TestClient(app).get("/api/env/check")

    assert response.status_code == 401


def test_cors_origins_are_configurable(monkeypatch):
    monkeypatch.setenv(
        "LITTLECRAWLER_CORS_ORIGINS",
        " https://admin.example.com/,http://localhost:3000 ",
    )

    assert get_cors_origins() == [
        "https://admin.example.com",
        "http://localhost:3000",
    ]
