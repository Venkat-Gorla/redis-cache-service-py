# 🚀 Redis Cache Service (Async Python Demo)

![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)
![Redis](https://img.shields.io/badge/Redis-7.x-red?logo=redis)
![Asyncio](https://img.shields.io/badge/Async-asyncio-green)
![Typer](https://img.shields.io/badge/CLI-Typer-orange)
![pytest](https://img.shields.io/badge/Tests-pytest%20%2B%20fakeredis-yellow)
![uv](https://img.shields.io/badge/Package%20Manager-uv-9cf)

A **modern async caching service** built on **Redis** to demonstrate:

- 🔁 Read/Write-through caching
- 📡 Event-driven invalidation using Redis **Pub/Sub**
- 🧩 Concurrency-safe async design with **asyncio**
- 🧰 Command-line interface powered by **Typer**
- ✅ Full test coverage with **pytest + fakeredis**

## 🧱 Quick Start

```bash
# Install dependencies
uv sync

# Explore CLI options
uv run src\cli.py --help
```

## 📂 Project Structure

```
redis-cache-service-py/
│
├── pyproject.toml
├── src/
│   ├── cli.py                    # CLI entrypoint (Typer)
│   ├── async_cli.py              # Async CLI variant
│   ├── redis_utils.py            # Redis helper functions
│   └── cache/
│       ├── manager.py            # Core cache read/write logic
│       ├── lock_table.py         # Per-key asyncio locks (anti-stampede)
│       └── stampede_prevention_demo.py  # Demo script
│
└── tests/
    ├── test_cache_manager.py     # Integration & stampede prevention tests
    ├── test_cli.py               # CLI command tests
    ├── test_redis_utils.py       # Redis utility tests
    └── conftest.py               # Pytest fixtures
```

## 🧮 Cache Stampede Prevention Demo

This project demonstrates **cache stampede mitigation** — preventing multiple concurrent clients from redundantly fetching the same missing key.

### 🔍 Problem

When a popular cache key expires or is invalidated, many concurrent requests may try to reload it at once. Without coordination, this can overwhelm the backend or data source.

### 💡 Solution

The service uses **per-key async locks** (`LockTable`) to ensure:

- The first requester acquires the lock and triggers the backend fetch.
- All other concurrent requests for the same key await the same lock.
- Once the result is fetched and cached, all waiting requests are served from the cache immediately.

This eliminates duplicate backend fetches and prevents stampedes.

### ⚙️ How It Works

Each key has a unique `asyncio.Lock` managed by a lightweight in-memory **LockTable**:

```python
# Simplified logic
async def get_or_set(key, loader):
    async with lock_table[key]:         # Only one fetch per key
        if key not in cache:
            cache[key] = await loader() # Load once
    return cache[key]
```

### 🚀 Run the Demo

```bash
uv run -m src.cache.stampede_prevention_demo
```

**Sample Output:**

```
All results: [22, 22, 22, 22, 22]
```

All concurrent requests share a **single backend call**, proving effective stampede prevention.

## 🧰 Tech Stack

| Component                    | Description                    |
| ---------------------------- | ------------------------------ |
| **Python 3.11+**             | Core language                  |
| **Redis (Upstash or local)** | Backend cache                  |
| **asyncio**                  | Async concurrency              |
| **Typer**                    | Modern CLI framework           |
| **pytest + fakeredis**       | Testing & mocking              |
| **uv**                       | Lightweight dependency manager |

## 🧪 Tests in Action

Run all tests:

```bash
uv run pytest -v
```

Example focus test for stampede prevention:

```bash
uv run pytest -k test_simple_cache_coalesces_requests -v
```

All tests simulate **concurrent clients, lock behavior, and cache invalidation**.

**Test Output:**

```
========================= test session starts =========================
collected 18 items

tests/test_cache_manager.py::test_lock_table_single_instance_per_key PASSED [  5%]
tests/test_cache_manager.py::test_lock_table_different_keys_create_different_locks PASSED [ 11%]
tests/test_cache_manager.py::test_simple_cache_coalesces_requests PASSED    [ 16%]
tests/test_cache_manager.py::test_simple_cache_reuses_cached_value PASSED   [ 22%]
tests/test_cache_manager.py::test_concurrent_different_keys_load_independently PASSED [ 27%]
tests/test_cli.py::test_ping PASSED                                         [ 33%]
tests/test_cli.py::test_set_key PASSED                                      [ 38%]
tests/test_cli.py::test_get_key_not_found PASSED                            [ 44%]
tests/test_cli.py::test_stream_trimming PASSED                              [ 50%]
tests/test_cli.py::test_stream_event_created PASSED                         [ 55%]
tests/test_cli.py::test_consume_pending_from_last PASSED                    [ 61%]
tests/test_redis_utils.py::test_async_ping_redis_success PASSED             [ 66%]
tests/test_redis_utils.py::test_async_set_key_success PASSED                [ 72%]
tests/test_redis_utils.py::test_async_get_key_success PASSED                [ 77%]
tests/test_redis_utils.py::test_async_get_key_missing PASSED                [ 83%]
tests/test_redis_utils.py::test_async_ping_redis_failure PASSED             [ 88%]
tests/test_redis_utils.py::test_async_set_key_failure PASSED                [ 94%]
tests/test_redis_utils.py::test_async_get_key_failure PASSED                [100%]

========================= 18 passed in 1.34s =========================
```

## 🔮 Future Enhancements

- 🔧 Extensible cache strategy architecture
- 🔐 Distributed lock mechanism using Redis for multi-instance setups
- 📊 Real-time metrics (hit/miss rates, contention) via Grafana or CLI dashboards
- 🧩 Pluggable invalidation policies and event hooks

### ⭐ If you found this project interesting — star it on GitHub!
