"""Real MCP without a model/API key. This is a protocol demo, not an agent demo."""
import asyncio
import importlib.metadata
import json
from datetime import datetime, timezone
from pathlib import Path
from tempfile import TemporaryDirectory

from agents import set_tracing_disabled

from agent_client import ROOT, discover, make_server, result_payload
from scripts.inspect_records import read_records


async def run():
    set_tracing_disabled(True)
    report = {"execution":"REAL_MCP_NO_MODEL", "utc":datetime.now(timezone.utc).isoformat(),
              "versions":{p:importlib.metadata.version(p) for p in ("fastmcp","mcp","openai-agents")}, "calls":[]}
    lead = dict(name="Protocol Demo",email="protocol@example.com",service_name="Project Clarity",
                notes="Scope a student project",follow_up_requested=True)
    cases = [
        ("get_service_details", {"service_name":"Project Clarity"}, "service_found",0),
        ("record_service_interest", lead, "interest_recorded",1),
        ("register_verified_service_interest", lead | {"email":"team@example.com","service_name":"Team Sprint"}, "interest_recorded",2),
        ("register_verified_service_interest", lead | {"service_name":"Unknown"}, "unknown_service",2),
        ("record_service_interest", lead, "already_recorded",2),
        ("record_service_interest", lead | {"email":"bad"}, "invalid_input",2),
        ("register_verified_service_interest", lead | {"email":"no@example.com","follow_up_requested":False}, "consent_required",2),
    ]
    with TemporaryDirectory(prefix="cedarbridge-protocol-") as temp:
        async with make_server(temp) as server:
            tools = await discover(server)
            report["tools"] = [t.model_dump(mode="json",by_alias=True) for t in tools]
            for name, args, code, count in cases:
                result = await server.call_tool(name,args)
                payload = result_payload(result)
                saved = read_records(Path(temp))
                passed = not result.is_error and payload.get("code")==code and len(saved)==count
                report["calls"].append({"tool":name,"result":payload,"record_count":len(saved),"passed":passed})
                print(f"[STORE PROOF] count={len(saved)}, expected={count}")
        report["client_closed"] = server.session is None
    report["passed"] = all(c["passed"] for c in report["calls"]) and report["client_closed"]
    (ROOT / "evidence/protocol.json").write_text(json.dumps(report,indent=2),encoding="utf-8")
    print("All protocol checks passed:", report["passed"])
    return report


if __name__ == "__main__":
    raise SystemExit(0 if asyncio.run(run())["passed"] else 1)
