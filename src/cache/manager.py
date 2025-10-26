from .lock_table import LockTable

class SimpleAsyncCache:
    def __init__(self):
        self._cache = {}
        self._lock_table = LockTable()

    async def get_or_set(self, key, loader):
        # quick path
        if key in self._cache:
            return self._cache[key]

        lock = await self._lock_table.get_lock(key)
        async with lock:
            # double check inside lock
            if key in self._cache:
                return self._cache[key]

            value = await loader()
            self._cache[key] = value
            return value
