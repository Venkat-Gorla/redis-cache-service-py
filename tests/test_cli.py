import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent / "src"))

import pytest
from typer.testing import CliRunner
import fakeredis
import cli

runner = CliRunner()

# vegorla: test coverage for stream functionality, shoule we use mock or real redis?

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
