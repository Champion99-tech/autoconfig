"""Configuration file loaders for supported formats with smart fallback."""
from __future__ import annotations
import json
from pathlib import Path
from typing import Dict, Any

from .env import load_env_file  # Smart .env loader


def load_json(path: Path) -> Dict[str, Any]:
    """Load JSON file safely, return empty dict on error."""
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"Warning: JSON decode error in {path}: {e}")
        return {}
    except OSError as e:
        print(f"Warning: Failed to read {path}: {e}")
        return {}


def load_yaml(path: Path) -> Dict[str, Any]:
    """Load YAML file safely, return empty dict if PyYAML not installed or error."""
    try:
        import yaml
    except ImportError:
        return {}
    if not path.exists():
        return {}
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except yaml.YAMLError as e:
        print(f"Warning: YAML parse error in {path}: {e}")
        return {}
    except OSError as e:
        print(f"Warning: Failed to read {path}: {e}")
        return {}


def load_toml(path: Path) -> Dict[str, Any]:
    """Load TOML file safely, return empty dict if toml not installed or error."""
    try:
        import toml
    except ImportError:
        return {}
    if not path.exists():
        return {}
    try:
        data = toml.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except (toml.TomlDecodeError, OSError) as e:
        print(f"Warning: TOML parse error in {path}: {e}")
        return {}


def load_dotenv_file(path: Path = Path(".env")) -> Dict[str, Any]:
    """Load .env file using smart loader from env.py."""
    return load_env_file(path)
