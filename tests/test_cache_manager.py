import asyncio
import pytest

from cache.lock_table import LockTable
from cache.manager import SimpleAsyncCache

@pytest.mark.asyncio
async def test_lock_table_single_instance_per_key():
    table = LockTable()

    # concurrent creation of same key lock
    async def get_lock():
        return await table.get_lock("alpha")

    locks = await asyncio.gather(*[get_lock() for _ in range(20)])

    # all coroutines must receive same lock instance
    assert all(l is locks[0] for l in locks)

@pytest.mark.asyncio
async def test_lock_table_different_keys_create_different_locks():
    table = LockTable()
    a_lock, b_lock = await asyncio.gather(
        table.get_lock("a"),
        table.get_lock("b"),
    )
    assert a_lock is not b_lock

@pytest.mark.asyncio
async def test_simple_cache_coalesces_requests():
    cache = SimpleAsyncCache()
    call_counter = {"count": 0}

    async def fake_loader():
        call_counter["count"] += 1
        # simulate slow backend call
        await asyncio.sleep(0.05)
        return "computed"

    # launch 50 concurrent requests for same key
    results = await asyncio.gather(
        *[cache.get_or_set("key1", fake_loader) for _ in range(50)]
    )

    # all must get same cached result
    assert all(r == "computed" for r in results)
    # backend loader called exactly once
    assert call_counter["count"] == 1

@pytest.mark.asyncio
async def test_simple_cache_reuses_cached_value():
    cache = SimpleAsyncCache()
    call_counter = {"count": 0}

    async def loader():
        call_counter["count"] += 1
        await asyncio.sleep(0)
        return "once"

    # first call computes and stores
    result1 = await cache.get_or_set("x", loader)
    # second call returns immediately from cache
    result2 = await cache.get_or_set("x", loader)

    assert result1 == "once"
    assert result2 == "once"

    # ensure loader called exactly once
    assert call_counter["count"] == 1, "Loader called multiple times — cache not reused"

@pytest.mark.asyncio
async def test_concurrent_different_keys_load_independently():
    cache = SimpleAsyncCache()
    seen = []

    async def loader_factory(val):
        async def loader():
            await asyncio.sleep(0.05)
            seen.append(val)
            return val
        return loader

    loader_a = await loader_factory("A")
    loader_b = await loader_factory("B")

    await asyncio.gather(
        cache.get_or_set("a", loader_a),
        cache.get_or_set("b", loader_b),
    )

    # both values should be loaded once, in any order
    assert sorted(seen) == ["A", "B"]
