"""CLI for AutoConfig."""
from __future__ import annotations
import argparse
import sys
from pathlib import Path
import importlib.util
from typing import Any, Optional

from .config import AutoConfig


def init_project() -> None:
    """Initialize project with .env.example and schema.py."""
    env_example = """API_KEY=
DEBUG=false
PORT=8000
"""
    Path(".env.example").write_text(env_example, encoding="utf-8")
    print("Created .env.example")

    schema_py = '''from autoconfig.validation import Validator

class AppConfig(Validator):
    API_KEY: str
    DEBUG: bool
    PORT: int
'''
    if not Path("schema.py").exists():
        Path("schema.py").write_text(schema_py, encoding="utf-8")
        print("Created schema.py")


def load_schema_from_file() -> Optional[Any]:
    """Dynamically load AppConfig schema from schema.py if available."""
    schema_file = Path("schema.py")
    if not schema_file.exists():
        return None
    try:
        spec = importlib.util.spec_from_file_location("schema", schema_file)
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return getattr(module, "AppConfig", None)
    except Exception as e:
        print(f"Warning: Failed to load schema.py: {e}", file=sys.stderr)
        return None


def main(argv: Optional[list[str]] = None) -> int:
    """Entry point for autoconfig CLI."""
    parser = argparse.ArgumentParser(prog="autoconfig", description="AutoConfig CLI")
    sub = parser.add_subparsers(dest="cmd", help="Available commands")

    # Initialize project
    sub.add_parser("init", help="Initialize project with .env.example and schema.py")

    # Generate .env.example
    gen = sub.add_parser("generate-example", help="Generate .env.example from schema")
    gen.add_argument("-o", "--out", default=".env.example", help="Output file path")

    # Dump current config to .env
    dump = sub.add_parser("dump-env", help="Dump current config to .env")
    dump.add_argument("-o", "--out", default=".env", help="Output file path")

    # Show merged config
    sub.add_parser("show", help="Print merged config")

    args = parser.parse_args(argv)

    schema = load_schema_from_file()
    cfg = AutoConfig(schema=schema)

    try:
        if args.cmd == "init":
            init_project()
        elif args.cmd == "generate-example":
            if schema is None:
                print("Error: schema.py not found or invalid.", file=sys.stderr)
                return 1
            cfg.generate_examples(Path(args.out))
            print(f"Wrote {args.out}")
        elif args.cmd == "dump-env":
            cfg.load()
            cfg.dump_env(Path(args.out))
            print(f"Wrote {args.out}")
        elif args.cmd == "show":
            config = cfg.load()
            import json
            print(json.dumps(config, indent=2, default=str))
        else:
            parser.print_help()
            return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
