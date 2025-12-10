"""Environment utilities: extraction, generation, and validation."""
from __future__ import annotations
import os
import re
from pathlib import Path
from typing import Dict, Any, Callable, Optional, Set

try:
    from dotenv import dotenv_values
except ImportError:
    dotenv_values = None


def _extract_env_names_from_code(code: str) -> Set[str]:
    """Extract env var names from Python code patterns."""
    keys = set()
    # Match os.getenv("KEY"), os.environ.get("KEY")
    pattern_get = r'(?:os\.(?:getenv|environ\.get))\s*\(\s*["\']([^"\']+)["\']'
    # Match os.environ["KEY"]
    pattern_bracket = r'os\.environ\s*\[\s*["\']([^"\']+)["\']\s*\]'
    keys.update(re.findall(pattern_get, code))
    keys.update(re.findall(pattern_bracket, code))
    return keys


def extract_env_from_project(
    search_paths: Optional[list[Path]] = None,
    extensions: tuple[str, ...] = (".py",)
) -> Dict[str, str]:
    """Scan project files to discover likely environment variable names."""
    if search_paths is None:
        search_paths = [Path.cwd()]

    found_keys: Set[str] = set()
    for base in search_paths:
        if not base.exists():
            continue
        for file in base.rglob("*"):
            if file.is_file() and file.suffix in extensions:
                try:
                    content = file.read_text(encoding="utf-8")
                    found_keys.update(_extract_env_names_from_code(content))
                except Exception:
                    continue

    return {k: "" for k in sorted(found_keys)}


def generate_env_example(
    schema: Dict[str, Any],
    path: Path = Path(".env.example"),
    interactive: bool = False
) -> None:
    """Generate .env.example from schema."""
    lines = []
    for key, info in schema.items():
        example = ""
        if isinstance(info, dict):
            example = str(info.get("example", ""))
        elif isinstance(info, str):
            pass  # type hint only
        lines.append(f"{key}={example}")

    if interactive:
        print(f"Generating {path.name}:")
        for line in lines:
            print(" ", line)
        if not input("Proceed? [Y/n]: ").lower().startswith("y"):
            print("Cancelled.")
            return

    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Written {path}")


def generate_env_file(values: Dict[str, Any], path: Path = Path(".env")) -> None:
    """Write values to .env file."""
    lines = [f"{k}={v}" for k, v in values.items()]
    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Generated {path}")


def validate_env(
    values: Dict[str, Any],
    validators: Optional[Dict[str, Callable[[Any], None]]] = None
) -> None:
    """Validate environment values using callables."""
    if not validators:
        return
    errors = []
    for key, validator in validators.items():
        if key in values:
            try:
                validator(values[key])
            except Exception as e:
                errors.append(f"{key}: {e}")
    if errors:
        raise ValueError("Environment validation failed:\n" + "\n".join(errors))


def load_env_file(path: Optional[Path] = None) -> Dict[str, str]:
    """Load environment variables from a .env file intelligently."""
    path = path or Path(".env")
    if dotenv_values:
        return dotenv_values(str(path)) or {}
    if not path.exists():
        return {}
    env = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, val = line.split("=", 1)
        env[key.strip()] = val.strip().strip("\"'")
    return env
