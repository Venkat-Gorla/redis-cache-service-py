"""
Simple single-process async lock table.
Prevents cache stampede by ensuring that concurrent requests
for the same key share one asyncio.Lock.
Locks are never deleted to keep implementation race-free.
"""

import asyncio

class LockTable:
    """Maintains a per-key asyncio.Lock for coalescing concurrent requests."""

    def __init__(self):
        self._locks: dict[str, asyncio.Lock] = {}
        self._table_lock = asyncio.Lock()  # protects creation of locks

    async def get_lock(self, key: str) -> asyncio.Lock:
        """
        Returns a shared asyncio.Lock for the given key.
        Safe for concurrent calls; only one lock is ever created per key.
        """
        async with self._table_lock:
            if key not in self._locks:
                self._locks[key] = asyncio.Lock()
            return self._locks[key]
