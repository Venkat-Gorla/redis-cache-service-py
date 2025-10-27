# Redis Cache Service

Async Redis-based caching service demonstrating:

- Read/Write-through caching
- Event-driven invalidation via Redis Pub/Sub
- Concurrency-safe async architecture with asyncio
- CLI interface (Typer)
- Unit + integration tests (pytest + fakeredis)

## 🧱 Quick Start

```bash
uv sync
uv run src\cli.py --help
```

## 📁 Project Structure

Pending: Please fill this section

## Cache Stampede Prevention Demo

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

Or interactively, from root folder:

```bash
redis-cache-service-py>uv run -m src.cache.stampede_prevention_demo

Sample output:
All results: [22, 22, 22, 22, 22]
```

All 5 concurrent tasks will share **a single backend call**, proving that cache stampede mitigation works.

## 🧰 Tech Stack

Pending, anything else to be added?
- Python
- uv for package management
- pytest
- Cloud based Redis (upstash)

## 🧪 Tests in Action

Pending, screen capture to be added

## ✅ Future Enhancements

- Extensible cache strategy architecture
- Extend locking to Redis for distributed processes
- Visualize metrics (hit/miss, lock contention) in Grafana or CLI
