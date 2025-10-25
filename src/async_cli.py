import os
import asyncio
import typer
from dotenv import load_dotenv
from redis import asyncio as aioredis
from redis_utils import async_ping_redis, async_set_key, async_get_key

app = typer.Typer()

load_dotenv()
redis_url = os.getenv("REDIS_URL")
if not redis_url:
    raise ValueError("REDIS_URL environment variable is not set")

redis_client = aioredis.from_url(redis_url)

@app.command()
def ping():
    typer.echo(asyncio.run(async_ping_redis(redis_client)))

@app.command()
def set_key(key: str, value: str):
    typer.echo(asyncio.run(async_set_key(redis_client, key, value)))

@app.command()
def get_key(key: str):
    typer.echo(asyncio.run(async_get_key(redis_client, key)))

if __name__ == "__main__":
    app()
