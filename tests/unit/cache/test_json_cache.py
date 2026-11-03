# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

"""Tests for the JsonCache backend."""

import pytest
from graphrag_cache.json_cache import JsonCache
from graphrag_storage.memory_storage import MemoryStorage


@pytest.mark.asyncio
async def test_json_cache_basic_operations():
    storage = MemoryStorage()
    cache = JsonCache(storage=storage)

    await cache.set("test_key", {"data": 123})
    assert await cache.has("test_key")
    assert await cache.get("test_key") == {"data": 123}

    await cache.delete("test_key")
    assert not await cache.has("test_key")
    assert await cache.get("test_key") is None


@pytest.mark.parametrize(
    "payload",
    [
        "not json",
        "[]",
        '"value"',
        "null",
        "42",
        '{"debug": "missing result"}',
    ],
)
@pytest.mark.asyncio
async def test_json_cache_removes_invalid_payload(payload: str):
    storage = MemoryStorage()
    cache = JsonCache(storage=storage)

    await storage.set("invalid_key", payload)
    assert await cache.has("invalid_key")

    assert await cache.get("invalid_key") is None
    assert not await cache.has("invalid_key")
