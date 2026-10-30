"""Read-only proof of persistence; contacts and notes are hidden by default."""
import argparse
import json
import sqlite3
from contextlib import closing
from pathlib import Path

from business import data_directory


def read_records(directory: Path) -> list[dict]:
    path = directory.resolve() / "interests.sqlite3"
    if not path.exists():
        return []
    with closing(sqlite3.connect(path.as_uri() + "?mode=ro", uri=True)) as db:
        db.row_factory = sqlite3.Row
        return [dict(row) for row in db.execute(
            "SELECT record_id, service_name, created_at, follow_up_requested FROM interests ORDER BY created_at")]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, default=data_directory())
    args = parser.parse_args()
    records = read_records(args.data_dir)
    print(json.dumps({"record_count":len(records), "records":records}, indent=2))


if __name__ == "__main__":
    main()
