# Redis Cache Service

Async Redis-based caching service demonstrating:

- Read/Write-through caching
- Event-driven invalidation via Redis Pub/Sub
- Concurrency-safe async architecture
- CLI interface (Typer)
- Unit + integration tests (pytest + fakeredis)

## 🧱 Quick Start

```bash
uv sync
uv run cachecli --help
```

## 🧠 Pending Features

- Async I/O with asyncio
- Pub/Sub for cache invalidation
- Extensible cache strategy architecture
- Metrics for cache performance

## 🧠 Cache Stampede Prevention Demo

This demo illustrates how the async cache service mitigates **cache stampede** — a common problem where multiple clients simultaneously request the same missing or invalidated key, causing redundant backend calls.

### 🔍 Problem

When a popular cache key expires or is invalidated, many concurrent requests may try to reload it at once. Without coordination, this can overwhelm the backend or data source.

### 💡 Solution

The cache uses a **per-key async lock** to ensure that:

- The first requester acquires the lock and triggers the backend fetch.
- All other concurrent requests for the same key await the same lock.
- Once the result is fetched and cached, all waiting requests are served from cache immediately.

This eliminates duplicate backend fetches and prevents stampedes.

### ⚙️ How It Works

Each key has a unique `asyncio.Lock` managed by a lightweight in-memory **LockTable**:

```python
# Pseudocode summary
async def get_or_set(key, loader):
    async with lock_table[key]:         # Only one fetch per key
        if key not in cache:
            cache[key] = await loader() # Load once
    return cache[key]
```

### 🚀 Run the Demo

You can simulate concurrent access with:

```bash
uv run pytest -k test_simple_cache_coalesces_requests -v
```

Or interactively:

```python
from cache.manager import SimpleAsyncCache
import asyncio, random

cache = SimpleAsyncCache()

async def slow_load():
    await asyncio.sleep(2)
    return random.randint(1, 100)

async def main():
    results = await asyncio.gather(
        *[cache.get_or_set("demo_key", slow_load) for _ in range(5)]
    )
    print("All results:", results)

asyncio.run(main())
```

All 5 concurrent tasks will share **a single backend call**, proving that cache stampede mitigation works.

---

### ✅ Next Steps

- Extend locking to Redis for distributed processes
- Add optional TTL jitter to reduce synchronized expirations
- Visualize metrics (hit/miss, lock contention) in Grafana or CLI

---
