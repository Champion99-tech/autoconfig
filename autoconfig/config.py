"""Pydantic-based validation layer for AutoConfig."""
from __future__ import annotations
from typing import Dict, Any
from pydantic import BaseModel, ValidationError


class Validator(BaseModel):
    """
    Base class for config validation schemas.

    Example:
        class AppConfig(Validator):
            PORT: int
            DEBUG: bool
    """
    class Config:
        extra = "forbid"  # Reject unknown keys

    @classmethod
    def validate(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate and cast data using Pydantic model.

        Args:
            data: Dictionary of values to validate.

        Returns:
            Validated and type-casted dictionary.

        Raises:
            ValueError: If validation fails, with detailed Pydantic errors.
        """
        try:
            instance = cls(**data)
            return instance.dict()
        except ValidationError as e:
            raise ValueError(f"Validation failed:\n{e}") from e
