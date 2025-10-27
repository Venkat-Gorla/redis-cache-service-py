# 🚀 Redis Cache Service (Async Python Demo)

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

## Cache Stampede Prevention Demo

This project demonstrates **cache stampede mitigation** — preventing multiple concurrent clients from redundantly fetching the same missing key.

### 🔍 Problem

When a popular cache key expires or is invalidated, many concurrent requests may try to reload it at once. Without coordination, this can overwhelm the backend or data source.

### 💡 Solution

The service uses **per-key async locks** (`LockTable`) to ensure:

- The first requester acquires the lock and triggers the backend fetch.
- All other concurrent requests for the same key await the same lock.
- Once the result is fetched and cached, all waiting requests are served from cache immediately.

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

---

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

Pending, screen capture to be added

## 🔮 Future Enhancements

- 🔧 Extensible cache strategy architecture
- 🔐 Distributed lock mechanism using Redis for multi-instance setups
- 📊 Real-time metrics (hit/miss rates, contention) via Grafana or CLI dashboards
- 🧩 Pluggable invalidation policies and event hooks

### ⭐ If you found this project interesting — star it on GitHub!
