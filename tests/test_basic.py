"""Basic tests for AutoConfig defaults and type casting."""
from autoconfig import AutoConfig


def test_load_defaults():
    """
    Test loading configuration with default values
    and automatic type casting.
    """
    cfg = AutoConfig(
        schema={"PORT": int, "DEBUG": bool},
        defaults={"PORT": 5000, "DEBUG": "false"}  # string to be casted to bool
    )
    loaded = cfg.load()

    assert loaded["PORT"] == 5000, "PORT should match the default integer value"
    assert loaded["DEBUG"] == False, "DEBUG string 'false' should be casted to False"
