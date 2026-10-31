"""Read-only proof of persistence; contacts and notes are hidden by default."""
import argparse
import json
import sqlite3
from contextlib import closing
from pathlib import Path

from dotenv import dotenv_values
from config import ROOT, data_directory


def configured_directory(value: str | Path | None = None) -> Path:
    # Read only directory configuration. Do not load an API credential into the inspector environment.
    import os
    selected = value if value is not None else os.getenv("CEDARBRIDGE_DATA_DIR")
    if selected is None:
        selected = dotenv_values(ROOT / ".env").get("CEDARBRIDGE_DATA_DIR")
    return data_directory(selected)


def read_records(directory: Path) -> list[dict]:
    path = data_directory(directory) / "interests.sqlite3"
    if not path.exists():
        return []
    with closing(sqlite3.connect(path.as_uri() + "?mode=ro", uri=True)) as db:
        db.row_factory = sqlite3.Row
        return [dict(row) for row in db.execute(
            "SELECT record_id, service_name, created_at, follow_up_requested FROM interests ORDER BY created_at")]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, help="Record directory; relative paths start at the C5 project.")
    args = parser.parse_args()
    records = read_records(configured_directory(args.data_dir))
    print(json.dumps({"record_count":len(records), "records":records}, indent=2))


if __name__ == "__main__":
    main()
