"""Tests for Pydantic-based Validator class."""
import pytest
from autoconfig.validation import Validator

# Skip tests if pydantic not installed
pytest.importorskip("pydantic")


class AppConfig(Validator):
    API_KEY: str
    DEBUG: bool
    PORT: int


def test_pydantic_validation_cast_and_types():
    """Test that Validator casts types correctly and preserves values."""
    raw = {"API_KEY": "key-1", "DEBUG": "true", "PORT": "8080"}
    validated = AppConfig.validate(raw)

    assert isinstance(validated["PORT"], int), "PORT should be casted to int"
    assert validated["PORT"] == 8080, "PORT value mismatch"
    assert validated["DEBUG"] == True, "DEBUG should be casted to True"
    assert validated["API_KEY"] == "key-1", "API_KEY value mismatch"


def test_pydantic_validation_failure():
    """Test that Validator raises ValueError on invalid data."""
    raw_invalid = {"API_KEY": 123, "DEBUG": "notbool", "PORT": "notint"}
    with pytest.raises(ValueError):
        AppConfig.validate(raw_invalid)
