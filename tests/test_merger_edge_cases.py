"""Tests for merge_sources function: deep and shallow merge behavior."""
from autoconfig.merger import merge_sources


def test_deep_merge():
    """Test deep merging of nested dictionaries."""
    base = {"db": {"host": "localhost", "port": 3306}, "mode": "dev"}
    override = {"db": {"port": 5432}, "mode": "prod"}
    result = merge_sources([base, override], deep=True)

    assert result["db"]["host"] == "localhost", "Nested key 'host' should be preserved"
    assert result["db"]["port"] == 5432, "Nested key 'port' should be overridden"
    assert result["mode"] == "prod", "Top-level key 'mode' should be overridden"


def test_shallow_merge():
    """Test shallow merge (last dictionary wins)."""
    low = {"A": {"x": 1}}
    high = {"A": {"y": 2}}
    result = merge_sources([low, high], deep=False)

    assert result["A"] == {"y": 2}, "Shallow merge should fully replace nested dictionary"
