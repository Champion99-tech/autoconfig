"""Type casting and parsing utilities for AutoConfig."""
from __future__ import annotations
from typing import Any, Union


def cast_value(value: Any, target_type: Union[type, str, None]) -> Any:
    """
    Cast a value to a target type intelligently.

    Args:
        value: The value to cast.
        target_type: The expected type or string representation ("int", "bool", etc.)

    Returns:
        The value casted to the target type.
    
    Raises:
        ValueError: If the value cannot be cast to the target type.
    """
    if value is None or target_type is None:
        return value
    if value == "":
        return None if target_type is not str else ""

    # Map string-based types to actual Python types
    if isinstance(target_type, str):
        mapping = {
            "int": int, "integer": int,
            "float": float,
            "bool": bool, "boolean": bool,
            "str": str, "string": str,
            "list": list, "array": list,
        }
        target_type = mapping.get(target_type.lower(), str)

    # Already correct type
    if isinstance(value, target_type):
        return value

    s = str(value).strip()

    try:
        if target_type is bool:
            lowered = s.lower()
            if lowered in ("1", "true", "yes", "on"):
                return True
            if lowered in ("0", "false", "no", "off"):
                return False
            raise ValueError(f"Cannot cast {value!r} to bool")
        elif target_type is int:
            return int(s)
        elif target_type is float:
            return float(s)
        elif target_type is list:
            return [part.strip() for part in s.split(",")] if s else []
        elif target_type is str:
            return s
        else:
            return target_type(s)
    except (ValueError, TypeError) as e:
        raise ValueError(f"Cannot cast {value!r} to {target_type}") from e
