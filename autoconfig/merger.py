"""Merge configuration sources with optional deep merging."""
from __future__ import annotations
from typing import Dict, Any, List


def _deep_merge(low: Dict[str, Any], high: Dict[str, Any]) -> Dict[str, Any]:
    """
    Recursively merge two dictionaries.

    Args:
        low: Base dictionary (lower priority)
        high: Dictionary to merge (higher priority)
    
    Returns:
        Merged dictionary with high-priority values overriding low-priority.
    """
    result = low.copy()
    for key, value in high.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = _deep_merge(result[key], value)
        else:
            result[key] = value
    return result


def merge_sources(
    sources: List[Dict[str, Any]],
    deep: bool = False
) -> Dict[str, Any]:
    """
    Merge multiple config sources.

    Args:
        sources: List of config dicts, ordered from lowest to highest priority.
        deep: If True, merge nested dicts recursively; else last value wins (shallow merge).

    Returns:
        Merged dictionary combining all sources.
    """
    if not sources:
        return {}

    if deep:
        merged = sources[0].copy()
        for source in sources[1:]:
            merged = _deep_merge(merged, source)
        return merged
    else:
        # Shallow merge: last source wins
        result: Dict[str, Any] = {}
        for source in sources:
            result.update(source)
        return result
