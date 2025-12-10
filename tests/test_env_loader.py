"""Tests for AutoConfig env utilities: generate and validate .env files."""
from pathlib import Path
import pytest
from autoconfig.env import generate_env_file, generate_env_example, validate_env


def test_generate_and_validate_env(tmp_path):
    """
    Test generating .env and .env.example files from schema,
    and validate environment values using validators.
    """
    schema = {
        "API_KEY": {"type": "str", "example": "xxx"},
        "DEBUG": {"type": "bool", "example": "false"},
    }
    values = {"API_KEY": "abc123", "DEBUG": "true"}

    env_path = tmp_path / ".env"
    example_path = tmp_path / ".env.example"

    # Generate example and actual env files
    generate_env_example(schema, path=example_path)
    generate_env_file(values, path=env_path)

    # Check .env content
    content = env_path.read_text()
    assert "API_KEY=abc123" in content, "API_KEY not written correctly in .env"
    assert "DEBUG=true" in content, "DEBUG not written correctly in .env"

    # Check .env.example content
    example_content = example_path.read_text()
    assert "API_KEY=xxx" in example_content, "API_KEY example missing in .env.example"
    assert "DEBUG=false" in example_content, "DEBUG example missing in .env.example"

    # Validator function
    def check_api_key(v):
        if not v or not str(v).startswith("abc"):
            raise ValueError("bad api key")

    # Should pass validation
    validate_env(values, validators={"API_KEY": check_api_key})

    # Should fail validation
    bad_values = {"API_KEY": "badkey", "DEBUG": "true"}
    with pytest.raises(ValueError, match="bad api key"):
        validate_env(bad_values, validators={"API_KEY": check_api_key})
