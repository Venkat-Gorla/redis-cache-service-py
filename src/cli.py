import os
import redis
import typer
from dotenv import load_dotenv

app = typer.Typer()

load_dotenv()
redis_url = os.getenv("REDIS_URL")
if not redis_url:
    raise ValueError("REDIS_URL environment variable is not set")

redis_client = redis.Redis.from_url(redis_url)

@app.command()
def ping():
    """Ping the Redis instance."""
    try:
        typer.echo("PONG" if redis_client.ping() else "Failed to ping Redis")
    except redis.exceptions.ConnectionError as e:
        typer.echo(f"Error: {e}")

@app.command()
def set_key(key: str, value: str):
    """Set a key-value pair in Redis."""
    try:
        redis_client.set(key, value)
        typer.echo(f"Key '{key}' set successfully.")
    except redis.exceptions.ConnectionError as e:
        typer.echo(f"Error: {e}")

@app.command()
def get_key(key: str):
    """Get a value by key from Redis."""
    try:
        value = redis_client.get(key)
        if value is None:
            typer.echo(f"Key '{key}' not found.")
        else:
            typer.echo(f"{key} = {value.decode('utf-8')}")
    except redis.exceptions.ConnectionError as e:
        typer.echo(f"Error: {e}")

@app.command()
def dummy():
    """Run a dummy test command."""
    typer.echo("Dummy function for testing.")

if __name__ == "__main__":
    app()
