import os
import asyncio
import typer
from dotenv import load_dotenv
from redis import asyncio as aioredis

app = typer.Typer()

load_dotenv()
redis_url = os.getenv("REDIS_URL")
if not redis_url:
    raise ValueError("REDIS_URL environment variable is not set")

redis_client = aioredis.from_url(redis_url)

async def async_ping_redis():
    try:
        pong = await redis_client.ping()
        return "PONG" if pong else "Failed to ping Redis"
    except Exception as e:
        return f"Error: {e}"

@app.command()
def ping():
    """Ping Redis asynchronously."""
    typer.echo(asyncio.run(async_ping_redis()))

async def async_set_key(key: str, value: str):
    try:
        await redis_client.set(key, value)
        return f"Key '{key}' set successfully."
    except Exception as e:
        return f"Error: {e}"

@app.command()
def set_key(key: str, value: str):
    """Set a key asynchronously."""
    typer.echo(asyncio.run(async_set_key(key, value)))

async def async_get_key(key: str):
    try:
        value = await redis_client.get(key)
        if value:
            return f"{key} = {value.decode()}"
        else:
            return f"Key '{key}' not found."
    except Exception as e:
        return f"Error: {e}"

@app.command()
def get_key(key: str):
    """Get a key asynchronously."""
    typer.echo(asyncio.run(async_get_key(key)))

if __name__ == "__main__":
    app()
