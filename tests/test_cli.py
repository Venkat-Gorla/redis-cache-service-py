import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent / "src"))

import pytest
from typer.testing import CliRunner
import fakeredis
import cli

runner = CliRunner()

@pytest.fixture(autouse=True)
def mock_redis(monkeypatch):
    fake_redis_client = fakeredis.FakeRedis()
    monkeypatch.setattr(cli, "redis_client", fake_redis_client)
    yield

def test_ping():
    result = runner.invoke(cli.app, ["ping"])
    assert result.exit_code == 0
    assert "PONG" in result.output

def test_set_key():
    result = runner.invoke(cli.app, ["set-key", "foo", "bar"])
    assert result.exit_code == 0
    assert (
        f"Key 'foo' set successfully and recorded invalidation "
        f"(trimmed to {cli.STREAM_MAXLEN})."
    ) in result.output

    # Verify the key was set
    result = runner.invoke(cli.app, ["get-key", "foo"])
    assert result.exit_code == 0
    assert "foo = bar" in result.output

def test_get_key_not_found():
    result = runner.invoke(cli.app, ["get-key", "nonexistent"])
    assert result.exit_code == 0
    assert "Key 'nonexistent' not found." in result.output

def test_stream_trimming(mock_redis):
    for i in range(cli.STREAM_MAXLEN + 5):
        runner.invoke(cli.app, ["set-key", f"k{i}", f"v{i}"])

    stream_len = cli.redis_client.xlen(cli.STREAM_KEY)
    assert stream_len <= cli.STREAM_MAXLEN

def test_stream_event_created(mock_redis):
    runner.invoke(cli.app, ["set-key", "alpha", "beta"])
    entries = cli.redis_client.xrange(cli.STREAM_KEY)
    assert len(entries) == 1
    msg_id, data = entries[0]
    assert data[b"key"].decode() == "alpha"

def test_consume_pending_from_last(mock_redis):
    """Ensure consuming from last ID reads nothing after full stream processed."""
    # Arrange: add a few messages into the stream
    for i in range(3):
        cli.redis_client.xadd(cli.STREAM_KEY, {"event": "invalidate", "key": f"key{i}"})

    result = runner.invoke(cli.app, ["consume-pending"])
    assert result.exit_code == 0
    assert "Last processed ID:" in result.output
    assert cli.redis_client.get(cli._LAST_PROCESSED_ID) is not None

    result = runner.invoke(cli.app, ["consume-pending-from-last"])
    assert result.exit_code == 0
    assert "No new events." in result.output
