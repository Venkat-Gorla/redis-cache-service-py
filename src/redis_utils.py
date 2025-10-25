async def async_ping_redis(client):
    """Ping Redis asynchronously."""
    try:
        pong = await client.ping()
        return "PONG" if pong else "Failed to ping Redis"
    except Exception as e:
        return f"Error: {e}"

async def async_set_key(client, key: str, value: str):
    """Set a key asynchronously."""
    try:
        await client.set(key, value)
        return f"Key '{key}' set successfully."
    except Exception as e:
        return f"Error: {e}"

async def async_get_key(client, key: str):
    """Get a key asynchronously."""
    try:
        value = await client.get(key)
        if value:
            return f"{key} = {value.decode()}"
        else:
            return f"Key '{key}' not found."
    except Exception as e:
        return f"Error: {e}"
