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
