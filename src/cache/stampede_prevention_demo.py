import asyncio, random
from .manager import SimpleAsyncCache

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
