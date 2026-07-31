"""Tests for AI Application Framework."""

import pytest
from zkai.apps.app import (
    AIApplication,
    ApplicationManifest,
    ApplicationPermissions,
    ApplicationRuntime,
    ApplicationSandbox,
)
from zkai.apps.registry import ApplicationStore


def test_ai_application_execution():
    manifest = ApplicationManifest(
        app_id="app_test",
        name="TestApp",
        version="1.0.0",
        description="A test application",
        author="Tester",
        entry_point="main.py",
        permissions=ApplicationPermissions(requested_capabilities=["filesystem"]),
    )
    app = AIApplication(manifest)
    runtime = ApplicationRuntime()

    res = runtime.run_app(app)
    assert "TestApp" in res
    assert app.lifecycle.is_running is True


def test_application_store_and_search():
    store = ApplicationStore()
    manifest = ApplicationManifest(
        app_id="code_editor",
        name="Code Editor",
        version="1.0.0",
        description="IDE Application for code generation",
        author="ZKAI",
        entry_point="editor.py",
    )
    app = AIApplication(manifest)
    store.install_app(app)

    results = store.search_apps("editor")
    assert len(results) == 1
    assert results[0].app_id == "code_editor"
