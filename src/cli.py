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
def dummy():
    """dummy test function."""
    typer.echo(f"dummy function for testing")

if __name__ == "__main__":
    app()
