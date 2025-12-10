"""Pydantic-based validation layer (optional)."""
from __future__ import annotations
from typing import Dict, Any
from pydantic import BaseModel, ValidationError


class Validator(BaseModel):
    """Base class for configuration validation schemas using Pydantic."""

    class Config:
        extra = "forbid"  # reject unknown keys

    @classmethod
    def validate(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate and cast data using Pydantic model.

        Args:
            data: Dictionary of values to validate.

        Returns:
            Dictionary of validated and casted values.

        Raises:
            ValueError: if validation fails.
        """
        try:
            instance = cls(**data)
            return instance.dict()
        except ValidationError as e:
            raise ValueError(f"Validation failed:\n{e}") from e
