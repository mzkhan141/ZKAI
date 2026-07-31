"""Tests for Web Desktop Dashboard."""

import pytest
from fastapi.testclient import TestClient
from zkai.web_desktop.server import app


def test_web_desktop_dashboard_and_status():
    client = TestClient(app)
    res_html = client.get("/")
    assert res_html.status_code == 200
    assert "ZKAI AI Operating System" in res_html.text
    assert "1. Conversation Center" in res_html.text

    res_status = client.get("/api/status")
    assert res_status.status_code == 200
    assert res_status.json()["status"] == "ok"
