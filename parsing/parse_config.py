import sys

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional, Tuple


ALLOWED_KEYS = {"WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"}


class ConfigError(ValueError):
    """Configuration parsing/validation errors."""


def read_raw_config(filepath: str | Path) -> Dict[str, str]:
    """Read a strict KEY=VALUE config file.

    Enforcement rules:
    - Non-empty lines must be exactly KEY=VALUE (one '=' minimum)
    - Lines starting with '#' or ';' are ignored as comments
    - Keys are upper-cased and must be one of ALLOWED_KEYS
    - Duplicate keys raise ConfigError
    - Empty keys or empty values raise ConfigError
    """
    path = Path(filepath)
    if not path.exists():
        raise ConfigError(f"Config file not found: {filepath}")

    out: Dict[str, str] = {}
    with path.open() as fh:
        for lineno, raw in enumerate(fh, start=1):
            line = raw.rstrip('\n')
            if not line.strip():
                continue
            stripped = line.lstrip()
            if stripped.startswith('#') or stripped.startswith(';'):
                continue

            if '=' not in line:
                msg = f"{path}:{lineno}: expected KEY=VALUE, got: {line}"
                raise ConfigError(msg)

            key, val = line.split('=', 1)
            key = key.strip().upper()
            val = val.strip()

            if not key:
                raise ConfigError(f"{path}:{lineno}: empty key")
            if not val:
                msg = f"{path}:{lineno}: empty value for key '{key}'"
                raise ConfigError(msg)
            if key not in ALLOWED_KEYS:
                msg = f"{path}:{lineno}: unexpected key '{key}'"
                raise ConfigError(msg)
            if key in out:
                raise ConfigError(f"{path}:{lineno}: duplicate key '{key}'")

            out[key] = val

    return out


@dataclass
class Config:
    width: int
    height: int
    entry: Tuple[int, int]
    exit: Tuple[int, int]
    output_file: str
    perfect: bool


def validate_width(value: Optional[str]) -> int:
    if value is None:
        raise ConfigError("WIDTH is required")
    try:
        w = int(value)
    except ValueError:
        raise ConfigError(f"WIDTH must be integer, got: {value}")
    if w <= 0:
        raise ConfigError("WIDTH must be positive")
    return w


def validate_height(value: Optional[str]) -> int:
    if value is None:
        raise ConfigError("HEIGHT is required")
    try:
        h = int(value)
    except ValueError:
        raise ConfigError(f"HEIGHT must be integer, got: {value}")
    if h <= 0:
        raise ConfigError("HEIGHT must be positive")
    return h


def _parse_coord(value: str) -> Tuple[int, int]:
    parts = [p.strip() for p in value.split(',')]
    if len(parts) != 2:
        msg = f"invalid coordinate, expected 'x,y', got: {value}"
        raise ConfigError(msg)
    try:
        x = int(parts[0])
        y = int(parts[1])
    except ValueError:
        msg = f"coordinates must be integers, got: {value}"
        raise ConfigError(msg)
    return x, y


def validate_entry(
    value: Optional[str], width: int, height: int
) -> Tuple[int, int]:
    if value is None:
        raise ConfigError("ENTRY is required")
    x, y = _parse_coord(value)
    if not (0 <= x < width and 0 <= y < height):
        msg = (f"ENTRY ({x}, {y}) out of bounds "
               f"for width={width}, height={height}")
        raise ConfigError(msg)
    return x, y


def validate_exit(
    value: Optional[str], width: int, height: int
) -> Tuple[int, int]:
    if value is None:
        raise ConfigError("EXIT is required")
    x, y = _parse_coord(value)
    if not (0 <= x < width and 0 <= y < height):
        msg = (f"EXIT ({x}, {y}) out of bounds "
               f"for width={width}, height={height}")
        raise ConfigError(msg)
    return x, y


def validate_output_file(value: Optional[str]) -> str:
    if value is None:
        raise ConfigError("OUTPUT_FILE is required")
    if not value:
        raise ConfigError("OUTPUT_FILE must not be empty")
    return value


def validate_perfect(value: Optional[str]) -> bool:
    if value is None:
        raise ConfigError("PERFECT is required")
    v = value.strip().lower()
    if v in ("true", "1", "yes", "y"):
        return True
    if v in ("false", "0", "no", "n"):
        return False
    msg = f"PERFECT must be boolean (true/false), got: {value}"
    raise ConfigError(msg)


def parse_config(filepath: str | Path) -> Config:
    raw = read_raw_config(filepath)
    width = validate_width(raw.get('WIDTH'))
    height = validate_height(raw.get('HEIGHT'))
    entry = validate_entry(raw.get('ENTRY'), width, height)
    exit_ = validate_exit(raw.get('EXIT'), width, height)
    output_file = validate_output_file(raw.get('OUTPUT_FILE'))
    perfect = validate_perfect(raw.get('PERFECT'))
    if entry == exit_:
        raise ConfigError("ENTRY and EXIT cannot be the same point")
    return Config(
        width=width,
        height=height,
        entry=entry,
        exit=exit_,
        output_file=output_file,
        perfect=perfect,
    )


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python -m parsing.parse_config <config-file>')
        raise SystemExit(2)
    cfg = parse_config(sys.argv[1])
    print(f"{cfg}")
