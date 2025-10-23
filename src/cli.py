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
STREAM_KEY = "cache_invalidation_stream"
STREAM_MAXLEN = 20  # keep last 20 messages only

@app.command()
def ping():
    """Ping the Redis instance."""
    try:
        typer.echo("PONG" if redis_client.ping() else "Failed to ping Redis")
    except redis.exceptions.ConnectionError as e:
        typer.echo(f"Error: {e}")

@app.command()
def set_key(key: str, value: str):
    """Set a key-value pair in Redis and record invalidation in stream."""
    try:
        redis_client.set(key, value)
        redis_client.xadd(STREAM_KEY, {"event": "invalidate", "key": key})
        redis_client.xtrim(STREAM_KEY, maxlen=STREAM_MAXLEN, approximate=True)
        typer.echo(
            f"Key '{key}' set successfully and recorded invalidation "
            f"(trimmed to {STREAM_MAXLEN})."
        )
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
def consume_pending(last_id: str = "0-0"):
    """Consume messages from the invalidation stream."""
    typer.echo(f"Reading events from {STREAM_KEY} starting at ID {last_id}")
    messages = redis_client.xread({STREAM_KEY: last_id}, count=None, block=1000)
    if not messages:
        typer.echo("No new events.")
        return

    last_id = print_messages(messages, last_id)

def print_messages(messages, last_id):
    for stream, events in messages:
        for msg_id, fields in events:
            key = fields.get(b"key", b"").decode()
            typer.echo(f"[EVENT] Invalidate cache for key: {key} (id={msg_id.decode()})")
            last_id = msg_id.decode()

    typer.echo(f"Last processed ID: {last_id}")
    return last_id

@app.command()
def show_stream():
    """Show recent stream messages."""
    entries = redis_client.xrange(STREAM_KEY, count=STREAM_MAXLEN)
    for msg_id, fields in entries:
        data = {k.decode(): v.decode() for k, v in fields.items()}
        typer.echo(f"{msg_id.decode()} -> {data}")

if __name__ == "__main__":
    app()
