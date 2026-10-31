"""Shared local path semantics; the MCP server never loads a credential file."""
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def data_directory(value: str | Path | None = None) -> Path:
    selected = value if value is not None else os.getenv("CEDARBRIDGE_DATA_DIR", "runtime")
    directory = Path(selected or "runtime")
    return (directory if directory.is_absolute() else ROOT / directory).resolve()
