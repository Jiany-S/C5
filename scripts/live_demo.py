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

from agent_client import ROOT, SetupError, safe_error, discover, make_agent, make_server
from terminal_ui import TerminalUI
from scripts.demo_cases import CASES
from scripts.demo_checks import assess_case
from scripts.inspect_records import read_records


def save_report(report: dict, output: Path) -> None:
    """Atomic snapshots prevent a partial JSON file from looking like valid evidence."""
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_suffix(output.suffix + ".tmp")
    temporary.write_text(json.dumps(report, indent=2), encoding="utf-8")
    temporary.replace(output)


async def run_demo(*, step=False, output: Path | None = None, trace=False,
                   ui: TerminalUI | None = None) -> dict:
    ui = ui or TerminalUI()
    load_dotenv(ROOT / ".env", override=False)
    set_tracing_disabled(True)
    run_id = str(uuid4())
    directory = ROOT / "runtime" / ("demo-" + run_id[:8])
    output = output or directory / "live_report.json"
    report = {"execution": "REAL_OPENAI_MODEL_REAL_MCP", "run_id":run_id,
              "state":"running", "passed":False, "utc": datetime.now(timezone.utc).isoformat(),
              "model": os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
              "versions": {p:importlib.metadata.version(p) for p in ("fastmcp","mcp","openai-agents","openai")},
              "data_dir": str(directory.relative_to(ROOT)), "cases": [],
              "prose_checks":"Heuristic checks; manually review final answers before submission."}
    save_report(report, output)  # Invalidate an explicitly selected older report BEFORE any call.
    ui.say(f"Evidence for this run: {output}")
    server = None
    active_case = None
    start = 0
    original_record_id = None
    try:
        if not os.getenv("OPENAI_API_KEY", "").strip():
            raise SetupError("OpenAI API key is missing. Configure C5/.env or your shell; protocol_demo works without a key.")
        async with make_server(directory, verbose=trace, ui=ui) as server:
            tools = await discover(server)
            report["tools"] = [t.name for t in tools]
            ui.welcome(report["model"], directory)
            ui.say("LIVE DEMO | Real OpenAI model + real MCP | 7 scenarios", style="cyan")
            ui.tools(tools)
            agent = make_agent(server)
            for index, case in enumerate(CASES, 1):
                ui.say(f"\n[{index}/{len(CASES)}] {case['id'].replace('_', ' ').title()}", style="bold cyan")
                if step:
                    try:
                        command = input("Enter to run | q to stop: ").strip().casefold()
                    except EOFError:
                        command = "q"
                    if command in {"q", "quit", "exit"}:
                        report["state"] = "cancelled"
                        break
                active_case = case
                start = len(server.events)
                ui.say("You: " + case["prompt"])
                # Independent conversations make each copy-paste prompt self-contained.
                result = await Runner.run(agent, case["prompt"], max_turns=8)
                events = server.events[start:]
                answer = str(result.final_output)
                saved = read_records(directory)
                checks = assess_case(case, events, answer, saved, original_record_id)
                if case["id"] == "action":
                    original_record_id = next((e["result"].get("record_id") for e in events if e["result"].get("created")), None)
                item = {"id":case["id"], "prompt":case["prompt"], "events":events,
                        "answer":answer, "record_count":len(saved), "checks":checks, "passed":all(checks.values())}
                report["cases"].append(item)
                save_report(report, output)
                active_case = None
                ui.answer(answer)
                ui.records(saved)
                failed = [name for name, passed in checks.items() if not passed]
                ui.say("Checks: " + ("PASS" if not failed else "REVIEW: " + ", ".join(failed)), style="green" if not failed else "yellow")
            else:
                report["state"] = "completed"
        report["passed"] = report["state"] == "completed" and len(report["cases"]) == len(CASES) and all(c["passed"] for c in report["cases"])
    except BaseException as error:
        report["state"] = "cancelled" if isinstance(error, (KeyboardInterrupt, asyncio.CancelledError)) else "failed"
        report["error_type"] = type(error).__name__  # No provider request body or raw exception string.
        if active_case:
            report["interrupted_case"] = {"id":active_case["id"], "events":server.events[start:] if server else []}
        raise
    finally:
        report["finished_utc"] = datetime.now(timezone.utc).isoformat()
        save_report(report, output)
    ui.say(f"\nDemo {report['state']}: {sum(c['passed'] for c in report['cases'])}/{len(CASES)} scenarios passed.")
    ui.say(f"Evidence saved: {output}")
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--step", action="store_true", help="Pause before each scenario for screen recording.")
    parser.add_argument("--trace", action="store_true", help="Include raw MCP JSON and server capability events.")
    parser.add_argument("--output", type=Path, help="Explicit report destination. Default: a new runtime/demo-.../live_report.json.")
    args = parser.parse_args()
    try:
        report = asyncio.run(run_demo(step=args.step, output=args.output, trace=args.trace))
    except KeyboardInterrupt:
        TerminalUI().say("Demo stopped. Partial evidence was preserved.")
        raise SystemExit(130)
    except Exception as exc:
        # Exception class is useful without disclosing provider bodies, key or contacts.
        TerminalUI().error(safe_error(exc) + "\nThe failed or partial run was preserved in its report.")
        raise SystemExit(1)
    raise SystemExit(0 if report["passed"] else 1)


if __name__ == "__main__":
    main()
