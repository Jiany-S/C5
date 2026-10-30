"""Real OpenAI model + Agents SDK + MCP. Each run uses a fresh local demo store."""
import argparse
import asyncio
import importlib.metadata
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from agents import Runner, set_tracing_disabled
from dotenv import load_dotenv

from agent_client import ROOT, discover, make_agent, make_server
from scripts.demo_cases import CASES
from scripts.inspect_records import read_records


async def run_demo(*, step=False, output: Path | None = None) -> dict:
    load_dotenv(ROOT / ".env", override=False)
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY is not configured.")
    set_tracing_disabled(True)
    directory = ROOT / "runtime" / ("demo-" + str(uuid4())[:8])
    report = {"execution": "REAL_OPENAI_MODEL_REAL_MCP", "utc": datetime.now(timezone.utc).isoformat(),
              "model": os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
              "versions": {p:importlib.metadata.version(p) for p in ("fastmcp","mcp","openai-agents","openai")},
              "data_dir": str(directory.relative_to(ROOT)), "cases": []}
    async with make_server(directory) as server:
        tools = await discover(server)
        report["tools"] = [t.name for t in tools]
        print("[ACTUAL MCP DISCOVERY] " + ", ".join(report["tools"]), flush=True)
        print("[LOCAL STORE] " + str(directory), flush=True)
        agent = make_agent(server)
        for case in CASES:
            if step:
                input(f"\nPress Enter for {case['id']} (real API call): ")
            print("\nUSER: " + case["prompt"], flush=True)
            start = len(server.events)
            # Independent conversations make each copy-paste prompt self-contained.
            result = await Runner.run(agent, case["prompt"], max_turns=8)
            events = server.events[start:]
            answer = str(result.final_output)
            saved = read_records(directory)
            checks = {"record_count":len(saved) == case["count"]}
            if case["tool"]:
                # A retry may use either idempotent writing interface. Both coordinate
                # the same persistence capability. The separate action/orchestration
                # scenarios still require their respective tool categories explicitly.
                allowed = {case["tool"]}
                if case["id"] == "repeat":
                    allowed.add("register_verified_service_interest")
                matching = [e for e in events if e["tool"] in allowed and e["result"].get("code") == case["code"]]
                checks["selected_tool_and_code"] = bool(matching)
                if matching and matching[-1]["result"].get("record_id"):
                    checks["answer_includes_actual_record_id"] = matching[-1]["result"]["record_id"] in answer
                    checks["no_booking_or_email_claim"] = "no" in answer.lower() and "appointment" in answer.lower() and "email" in answer.lower()
            else:
                checks["invalid_email_not_saved"] = not any(e["result"].get("created") for e in events)
            if case["id"] in {"data", "information_with_contact"}:
                checks["only_read_tool_used"] = bool(events) and all(e["tool"] == "get_service_details" for e in events)
                checks["answer_grounded_price"] = ("15" if case["id"] == "data" else "30") in answer
            if case["id"] == "unknown":
                checks["no_record_claim"] = "moon camp" in answer.lower() and any(w in answer.lower() for w in ("not", "couldn", "unable", "isn't"))
            item = {"id":case["id"], "prompt":case["prompt"], "events":events,
                    "answer":answer, "record_count":len(saved), "checks":checks, "passed":all(checks.values())}
            report["cases"].append(item)
            print("MIRA: " + answer, flush=True)
            print("[READ-ONLY STORE PROOF] " + json.dumps({"record_count":len(saved), "records":saved}), flush=True)
            print("[CHECKS] " + json.dumps(checks), flush=True)
    report["passed"] = all(case["passed"] for case in report["cases"])
    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"[FINAL LIVE VALIDATION] {sum(c['passed'] for c in report['cases'])}/{len(report['cases'])} scenarios passed.", flush=True)
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--step", action="store_true", help="Pause before each scenario for screen recording.")
    parser.add_argument("--output", type=Path, default=ROOT / "evidence/live_agent.json")
    args = parser.parse_args()
    try:
        report = asyncio.run(run_demo(step=args.step, output=args.output))
    except Exception as exc:
        # Exception class is useful without disclosing provider bodies, key or contacts.
        print(f"Live run failed ({type(exc).__name__}). Check credentials, model access or network.", file=sys.stderr)
        raise SystemExit(1)
    raise SystemExit(0 if report["passed"] else 1)


if __name__ == "__main__":
    main()
