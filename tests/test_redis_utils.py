"""Unit tests for redis_utils async functions using fakeredis."""

import pytest
import pytest_asyncio
import fakeredis.aioredis
from redis_utils import async_ping_redis, async_set_key, async_get_key

@pytest_asyncio.fixture
async def fake_redis_client():
    """Fixture for a fake async Redis client."""
    client = await fakeredis.aioredis.FakeRedis()
    yield client
    await client.aclose()

@pytest.mark.asyncio
async def test_async_ping_redis_success(fake_redis_client):
    result = await async_ping_redis(fake_redis_client)
    assert result == "PONG"

@pytest.mark.asyncio
async def test_async_ping_redis_failure(monkeypatch):
    async def mock_ping():
        raise Exception("Ping failed")

    class FakeClient:
        async def ping(self):
            return await mock_ping()

    result = await async_ping_redis(FakeClient())
    assert "Error: Ping failed" in result

@pytest.mark.asyncio
async def test_async_set_key_success(fake_redis_client):
    result = await async_set_key(fake_redis_client, "foo", "bar")
    assert result == "Key 'foo' set successfully."
    assert await fake_redis_client.get("foo") == b"bar"

@pytest.mark.asyncio
async def test_async_set_key_failure(monkeypatch):
    async def mock_set(key, value):
        raise Exception("Set failed")

    class FakeClient:
        async def set(self, key, value):
            return await mock_set(key, value)

    result = await async_set_key(FakeClient(), "foo", "bar")
    assert "Error: Set failed" in result

@pytest.mark.asyncio
async def test_async_get_key_success(fake_redis_client):
    await fake_redis_client.set("mykey", "myvalue")
    result = await async_get_key(fake_redis_client, "mykey")
    assert result == "mykey = myvalue"

@pytest.mark.asyncio
async def test_async_get_key_missing(fake_redis_client):
    result = await async_get_key(fake_redis_client, "missing")
    assert result == "Key 'missing' not found."

@pytest.mark.asyncio
async def test_async_get_key_failure(monkeypatch):
    async def mock_get(key):
        raise Exception("Get failed")

    class FakeClient:
        async def get(self, key):
            return await mock_get(key)

    result = await async_get_key(FakeClient(), "foo")
    assert "Error: Get failed" in result
