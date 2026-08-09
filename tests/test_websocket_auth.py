from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient
from starlette.websockets import WebSocketDisconnect

from api.main import app


@pytest.mark.parametrize("path", ["/api/ws/logs", "/api/ws/status"])
def test_websocket_rejects_missing_token(path):
    with pytest.raises(WebSocketDisconnect) as exc_info:
        with TestClient(app).websocket_connect(path):
            pass

    assert exc_info.value.code == 1008


def test_log_websocket_accepts_valid_token():
    user = {"id": 7, "username": "tester", "is_active": True}

    with (
        patch("api.routers.websocket.verify_token", return_value={"user_id": 7}),
        patch("api.routers.websocket.get_user_by_id", return_value=user),
        TestClient(app).websocket_connect("/api/ws/logs?token=valid") as websocket,
    ):
        websocket.send_text("ping")
        assert websocket.receive_text() == "pong"
