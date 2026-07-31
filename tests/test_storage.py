"""Tests for Unified Storage Framework components."""

import pytest
from zkai.storage.blob import BlobStore
from zkai.storage.object_store import ObjectStore
from zkai.storage.cache_store import CacheStore
from zkai.storage.session_store import SessionStore
from zkai.storage.provider import StorageProvider


def test_blob_store(tmp_path):
    store = BlobStore(root_dir=tmp_path / "blobs")
    key = store.put(b"Hello Blob Data")
    assert key is not None
    data = store.get(key)
    assert data == b"Hello Blob Data"


def test_object_store(tmp_path):
    store = ObjectStore(root_dir=tmp_path / "objs")
    store.put_object("user_1", {"name": "Alice", "role": "admin"})
    obj = store.get_object("user_1")
    assert obj["name"] == "Alice"


def test_cache_store():
    cache = CacheStore(default_ttl_seconds=10.0)
    cache.set("k1", "v1")
    assert cache.get("k1") == "v1"


def test_session_store():
    sessions = SessionStore()
    s_id = sessions.create_session({"user": "bob"})
    s_data = sessions.get_session(s_id)
    assert s_data["user"] == "bob"


def test_storage_provider():
    provider = StorageProvider()
    assert provider.auto_select_backend("blob") is not None
