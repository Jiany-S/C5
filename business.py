"""Local CedarBridge capabilities. No MCP registration and no model/API calls here."""
from __future__ import annotations

import json
import logging
import os
import re
import sqlite3
from contextlib import closing
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal
from uuid import uuid4

from pydantic import BaseModel, ConfigDict

ROOT = Path(__file__).resolve().parent
LOGGER = logging.getLogger("cedarbridge")


class Service(BaseModel):
    name: str
    duration_minutes: int
    price_usd: int
    price_unit: str
    max_students: int
    description: str


class Step(BaseModel):
    capability: Literal["get_service_details", "record_service_interest"]
    code: str


class ToolResult(BaseModel):
    """Stable v1 envelope. Error/skipped results never imply successful persistence."""
    model_config = ConfigDict(extra="forbid")
    schema_version: Literal["1.0"] = "1.0"
    status: Literal["ok", "error", "skipped"]
    code: str
    message: str
    service: Service | None = None
    record_id: str | None = None
    created: bool = False
    steps: list[Step] = []
    available_services: list[str] = []
    context: dict[str, str | bool | list[str]] = {}


CATALOG = json.loads((ROOT / "business_data" / "services.json").read_text(encoding="utf-8"))
SERVICES = {s["name"].casefold(): Service(**s) for s in CATALOG["services"]}


def event(capability: str, code: str, record_id: str | None = None) -> None:
    """Log outcomes, never contact information, notes, credentials or SQL errors."""
    LOGGER.info(json.dumps({"event": "capability_result", "pid": os.getpid(),
                            "capability": capability, "code": code, "record_id": record_id}))


def lookup_service(service_name: str) -> ToolResult:
    """Read immutable local catalog only; never opens or creates the record store."""
    service = SERVICES.get(" ".join(service_name.split()).casefold())
    if not service:
        result = ToolResult(status="error", code="unknown_service", message="Service not found. Choose a published service.",
                            available_services=[s.name for s in SERVICES.values()])
    else:
        result = ToolResult(status="ok", code="service_found", message="Published fictional teaching data.", service=service,
                            context={k: v for k, v in CATALOG.items() if k != "services"})
    event("get_service_details", result.code)
    return result


def data_directory() -> Path:
    directory = Path(os.environ.get("CEDARBRIDGE_DATA_DIR", "runtime"))
    return directory if directory.is_absolute() else ROOT / directory


def record_interest(name: str, email: str, service_name: str, notes: str,
                    follow_up_requested: bool) -> ToolResult:
    """Insert at most one lead per normalized email/service, atomically across processes."""
    def finish(result: ToolResult) -> ToolResult:
        event("record_service_interest", result.code, result.record_id)
        return result

    if follow_up_requested is not True:
        return finish(ToolResult(status="skipped", code="consent_required", message="No record saved: explicit follow-up request required."))
    name, email, notes = name.strip(), email.strip().lower(), notes.strip()
    # Deliberately conservative ASCII email syntax; no network or deliverability check.
    valid_email = (len(email) <= 254 and re.fullmatch(
        r"[a-z0-9](?:[a-z0-9.!#$%&'*+/=?^_`{|}~-]*[a-z0-9])?@"
        r"(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z]{2,63}", email)
        and ".." not in email and ".@" not in email)
    if not (1 <= len(name) <= 100 and 1 <= len(notes) <= 1000 and valid_email):
        return finish(ToolResult(status="error", code="invalid_input",
                                message="Provide a name (1-100 characters), valid ASCII email, and notes (1-1000 characters)."))
    service = SERVICES.get(" ".join(service_name.split()).casefold())
    if service is None:
        return finish(ToolResult(status="error", code="unknown_service", message="Cannot record interest for an unpublished service."))
    try:
        directory = data_directory()
        directory.mkdir(parents=True, exist_ok=True)
        # UNIQUE and INSERT ON CONFLICT live in one database transaction: a read-then-write
        # check in Python alone would race across two separate MCP server processes.
        with closing(sqlite3.connect(directory / "interests.sqlite3", timeout=10)) as db, db:
            db.execute("""CREATE TABLE IF NOT EXISTS interests (
                record_id TEXT PRIMARY KEY, name TEXT NOT NULL, email TEXT NOT NULL,
                service_name TEXT NOT NULL, notes TEXT NOT NULL, created_at TEXT NOT NULL,
                follow_up_requested INTEGER NOT NULL CHECK (follow_up_requested = 1),
                UNIQUE(email, service_name))""")
            record_id = str(uuid4())
            cursor = db.execute("""INSERT INTO interests VALUES (?, ?, ?, ?, ?, ?, 1)
                ON CONFLICT(email, service_name) DO NOTHING""",
                (record_id, name, email, service.name, notes, datetime.now(timezone.utc).isoformat()))
            created = cursor.rowcount == 1
            row = db.execute("SELECT record_id FROM interests WHERE email=? AND service_name=?",
                             (email, service.name)).fetchone()
            assert row is not None
            record_id = row[0]
        return finish(ToolResult(status="ok", code="interest_recorded" if created else "already_recorded",
                                message=("Follow-up interest saved locally." if created else "Existing interest retained; no new record or update.")
                                + " No appointment booked, payment taken, or email sent.",
                                record_id=record_id, created=created))
    except (OSError, sqlite3.Error):
        # Never return exception strings: they can contain local paths or input data.
        return finish(ToolResult(status="error", code="storage_error", message="Unable to confirm persistence. Retry the same request safely."))


def register_verified_interest(name: str, email: str, service_name: str, notes: str,
                               follow_up_requested: bool) -> ToolResult:
    """Coordinate the same two capabilities exposed by the Data and Action tools."""
    lookup = lookup_service(service_name)
    steps = [Step(capability="get_service_details", code=lookup.code)]
    if lookup.status != "ok":
        result = lookup.model_copy(update={"steps": steps})
    elif follow_up_requested is not True:
        result = ToolResult(status="skipped", code="consent_required", message="Service verified. No record saved: explicit follow-up request required.",
                            service=lookup.service, steps=steps)
    else:
        action = record_interest(name, email, lookup.service.name, notes, follow_up_requested)
        steps.append(Step(capability="record_service_interest", code=action.code))
        result = action.model_copy(update={"service": lookup.service, "steps": steps})
    event("register_verified_service_interest", result.code, result.record_id)
    return result
