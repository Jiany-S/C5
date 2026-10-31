"""Every tool assertion here uses a real FastMCP subprocess via SDK stdio MCP."""
import asyncio
import json
import sqlite3
from contextlib import closing
from pathlib import Path

import pytest

from agent_client import ROOT, TOOL_NAMES, discover, make_server, result_payload

LEAD = dict(name="Demo Student", email="demo@example.com", service_name="Project Clarity",
            notes="Scope my student project", follow_up_requested=True)


def rows(directory: Path) -> list:
    path = directory / "interests.sqlite3"
    if not path.exists():
        return []
    with closing(sqlite3.connect(path)) as db:
        return db.execute("SELECT record_id,name,email,service_name,notes FROM interests").fetchall()


async def call(server, tool_name, **args):
    result = await server.call_tool(tool_name, args)
    assert not result.is_error
    return result_payload(result)


async def test_start_connect_and_exact_schemas(server):
    tools = await discover(server)
    assert {t.name for t in tools} == TOOL_NAMES
    for t in tools:
        schema = t.input_schema
        fields = {"service_name"} if t.name == "get_service_details" else set(LEAD)
        assert schema["type"] == "object"
        assert set(schema["properties"]) == fields
        assert set(schema["required"]) == fields
        assert all(p.get("description") for p in schema["properties"].values())
        assert schema["properties"]["service_name"]["type"] == "string"
        if t.name != "get_service_details":
            assert schema["properties"]["follow_up_requested"]["type"] == "boolean"
        category = {"get_service_details":"DATA", "record_service_interest":"ACTION",
                    "register_verified_service_interest":"ORCHESTRATION"}[t.name]
        assert t.description.startswith(category + ":")
        assert t.output_schema["properties"]["status"]


@pytest.mark.parametrize("name,price,minutes", [("Project Clarity",15,30),("Prototype Clinic",30,60),("Team Sprint",60,90)])
async def test_known_data_is_read_only(server, tmp_path, name, price, minutes):
    before = (ROOT / "business_data/services.json").read_bytes()
    result = await call(server, "get_service_details", service_name=name.lower())
    assert result["status"] == "ok"
    assert result["service"]["price_usd"] == price
    assert result["service"]["duration_minutes"] == minutes
    assert not (tmp_path / "records").exists()
    assert (ROOT / "business_data/services.json").read_bytes() == before


async def test_unknown_service_and_recovery(server, tmp_path):
    r = await call(server, "get_service_details", service_name="Moon Camp")
    assert r["code"] == "unknown_service" and len(r["available_services"]) == 3
    assert not rows(tmp_path / "records")
    assert (await call(server, "get_service_details", service_name="Team Sprint"))["status"] == "ok"


async def test_action_persists_and_duplicate_is_stable(server, tmp_path):
    first = await call(server, "record_service_interest", **LEAD)
    second = await call(server, "record_service_interest", **(LEAD | {"email":"DEMO@example.com", "notes":"Changed notes"}))
    assert first["created"] and first["code"] == "interest_recorded"
    assert second["code"] == "already_recorded" and not second["created"]
    assert first["record_id"] == second["record_id"]
    assert first["record_id"] in first["message"] and second["record_id"] in second["message"]
    saved = rows(tmp_path / "records")
    assert len(saved) == 1 and saved[0] == (first["record_id"],LEAD["name"],LEAD["email"],LEAD["service_name"],LEAD["notes"])


@pytest.mark.parametrize("changes", [{"email":"broken"},{"email":"a..b@example.com"},
                                    {"email":"demo@" + "a"*64 + ".com"},
                                    {"name":" "},{"notes":" "},{"service_name":"Missing"}])
async def test_action_domain_validation_never_writes(server, tmp_path, changes):
    result = await call(server, "record_service_interest", **(LEAD | changes))
    assert result["status"] == "error" and not result["created"]
    assert not (tmp_path / "records").exists()


async def test_email_domain_label_boundary(server, tmp_path):
    result = await call(server, "record_service_interest", **(LEAD | {"email":"demo@" + "a"*63 + ".com"}))
    assert result["created"] and len(rows(tmp_path / "records")) == 1


@pytest.mark.parametrize("changes", [{"name":""},{"email":None},{"follow_up_requested":"yes"},{"notes":"x"*1001}])
async def test_mcp_schema_validation_rejects(server, tmp_path, changes):
    r = await server.call_tool("record_service_interest", LEAD | changes)
    assert r.is_error
    assert not rows(tmp_path / "records")


@pytest.mark.parametrize("missing", list(LEAD))
async def test_missing_required_fields(server, tmp_path, missing):
    args = {k:v for k,v in LEAD.items() if k != missing}
    assert (await server.call_tool("record_service_interest", args)).is_error
    assert not rows(tmp_path / "records")


async def test_orchestration_real_lookup_then_action(server, tmp_path):
    result = await call(server, "register_verified_service_interest", **LEAD)
    assert result["status"] == "ok" and result["created"]
    assert result["steps"] == [
        {"capability":"get_service_details", "code":"service_found"},
        {"capability":"record_service_interest", "code":"interest_recorded"}]
    assert rows(tmp_path / "records")[0][0] == result["record_id"]


async def test_failed_lookup_stops_action(server, tmp_path):
    result = await call(server, "register_verified_service_interest", **(LEAD | {"service_name":"Missing"}))
    assert result["code"] == "unknown_service"
    assert result["steps"] == [{"capability":"get_service_details", "code":"unknown_service"}]
    assert not (tmp_path / "records").exists()


@pytest.mark.parametrize("tool", ["record_service_interest", "register_verified_service_interest"])
async def test_no_consent_no_side_effect(server, tmp_path, tool):
    result = await call(server, tool, **(LEAD | {"follow_up_requested":False}))
    assert result["code"] == "consent_required" and not result["created"]
    assert not (tmp_path / "records").exists()


async def test_storage_failure_is_safe(server, tmp_path):
    (tmp_path / "records").write_text("blocked", encoding="utf-8")
    r = await call(server, "record_service_interest", **LEAD)
    assert r["code"] == "storage_error" and r["record_id"] is None
    assert str(tmp_path) not in json.dumps(r)
    assert LEAD["email"] not in json.dumps(r)
    assert (await call(server, "get_service_details", service_name="Team Sprint"))["status"] == "ok"


async def test_concurrent_servers_and_restart_deduplicate(tmp_path):
    directory = tmp_path / "records"
    async with make_server(directory, verbose=False) as a, make_server(directory, verbose=False) as b:
        results = await asyncio.gather(call(a,"record_service_interest",**LEAD), call(b,"register_verified_service_interest",**LEAD))
        assert sum(r["created"] for r in results) == 1
        assert results[0]["record_id"] == results[1]["record_id"]
    async with make_server(directory, verbose=False) as c:
        assert (await call(c,"record_service_interest",**LEAD))["code"] == "already_recorded"
    assert len(rows(directory)) == 1


async def test_connections_close_on_exception_and_release_store(tmp_path):
    server = make_server(tmp_path, verbose=False)
    with pytest.raises(RuntimeError, match="deliberate"):
        async with server:
            await call(server, "record_service_interest", **LEAD)
            raise RuntimeError("deliberate")
    assert server.session is None
    from scripts.inspect_records import read_records
    assert len(read_records(tmp_path)) == 1
    # Windows refuses this unlink if either server or inspector leaks an open handle.
    (tmp_path / "interests.sqlite3").unlink()
    assert not (tmp_path / "interests.sqlite3").exists()
