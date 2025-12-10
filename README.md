# AutoConfig

Lightweight, unified config loader for Python projects.

## Features
- Reads `.env`, `JSON`, `YAML`, `TOML`
- Merges sources with precedence (`.env` < `os.environ`)
- Supports **deep merging** of nested configs
- Type casting & validation (via dict schema or Pydantic)
- Static analysis to extract `.env` keys from code
- CLI: `init`, `generate-example`, `dump-env`, `show`

## Install

```bash
pip install autoconfig[yaml,toml,env]  # or just autoconfig for minimal
```

## Usage

```python
from autoconfig import AutoConfig

schema = {
    "PORT": int,
    "DEBUG": {"type": "bool", "example": "false"}
}

cfg = AutoConfig(schema=schema, defaults={"PORT": 8000})
config = cfg.load()
print(config["PORT"])  # auto-cast to int
```

Or with Pydantic:

```python
# schema.py
from autoconfig.validation import Validator
class AppConfig(Validator):
    PORT: int
    DEBUG: bool
```

Then:

```python
from schema import AppConfig
cfg = AutoConfig(schema=AppConfig)
cfg.load()
```
