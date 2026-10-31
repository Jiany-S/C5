"""Evidence must stay truthful on failures, cancellation and contradictory model prose."""
import json
from types import SimpleNamespace

import pytest

import scripts.live_demo as demo
from scripts.demo_cases import CASES
from scripts.demo_checks import assess_case, claims_external_effect
from tests.test_cli import capture_ui


@pytest.mark.parametrize("answer", [
    "No problem. Your appointment is booked and email sent.",
    "No appointment was booked, but an email was sent.",
    "Note: we booked your appointment and sent you an email.",
])
def test_contradictory_external_effect_claims_are_rejected(answer):
    assert claims_external_effect(answer)


def test_unknown_service_answer_cannot_claim_success():
    case = next(c for c in CASES if c["id"] == "unknown")
    events = [{"tool":case["tool"], "result":{"code":"unknown_service", "created":False}, "is_error":False}]
    checks = assess_case(case, events, "Moon Camp is not published. I saved your interest.", [{},{}])
    assert not checks["no_successful_record_claim"]
    assert assess_case(case, events, "Moon Camp is not published. No interest was saved.", [{},{}])["no_successful_record_claim"]


def test_wrong_price_cannot_pass_by_substring():
    case = CASES[0]
    events = [{"tool":case["tool"], "result":{"code":"service_found", "created":False}, "is_error":False}]
    assert not assess_case(case, events, "Project Clarity costs $150 for 30 minutes.", [])["answer_grounded_price"]
    assert assess_case(case, events, "Project Clarity costs 15 USD for 30 minutes.", [])["answer_grounded_price"]


async def test_missing_key_invalidates_explicit_old_passing_report(monkeypatch, tmp_path):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.setattr(demo, "load_dotenv", lambda *a, **k: None)
    output = tmp_path / "report.json"
    output.write_text('{"passed":true,"state":"completed"}', encoding="utf-8")
    ui, _ = capture_ui()
    with pytest.raises(demo.SetupError):
        await demo.run_demo(output=output, ui=ui)
    report = json.loads(output.read_text(encoding="utf-8"))
    assert report["state"] == "failed" and report["passed"] is False
    assert report["error_type"] == "SetupError" and not report["cases"]


async def test_midrun_failure_preserves_completed_mcp_calls(monkeypatch, tmp_path):
    monkeypatch.setenv("OPENAI_API_KEY", "synthetic-demo-key")
    monkeypatch.setattr(demo, "ROOT", tmp_path)
    count = 0

    async def runner(agent, prompt, **kwargs):
        nonlocal count
        count += 1
        if count == 3:
            raise RuntimeError("private-failure-detail")
        server = agent.mcp_servers[0]
        args = {"service_name":"Project Clarity"} if count == 1 else dict(
            name="Demo Student",email="demo@example.com",service_name="Project Clarity",
            notes="Plan project",follow_up_requested=True)
        result = await server.call_tool("get_service_details" if count == 1 else "record_service_interest", args)
        payload = server.events[-1]["result"]
        answer = "Project Clarity costs 15 USD for 30 minutes." if count == 1 else (
            f"Recorded {payload['record_id']}. No appointment booked or email sent.")
        return SimpleNamespace(final_output=answer)

    monkeypatch.setattr(demo.Runner, "run", runner)
    output = tmp_path / "report.json"
    ui, _ = capture_ui()
    with pytest.raises(RuntimeError):
        await demo.run_demo(output=output, ui=ui)
    report = json.loads(output.read_text(encoding="utf-8"))
    assert report["state"] == "failed" and not report["passed"]
    assert len(report["cases"]) == 2 and report["cases"][-1]["record_count"] == 1
    assert report["interrupted_case"]["id"] == "orchestration"
    assert "private-failure-detail" not in output.read_text(encoding="utf-8")


async def test_demo_eof_cancels_before_model_call(monkeypatch, tmp_path):
    monkeypatch.setenv("OPENAI_API_KEY", "synthetic-demo-key")
    monkeypatch.setattr(demo, "ROOT", tmp_path)
    monkeypatch.setattr("builtins.input", lambda _: (_ for _ in ()).throw(EOFError()))

    async def must_not_run(*args, **kwargs):
        pytest.fail("EOF before the first step must not cause an API call")

    monkeypatch.setattr(demo.Runner, "run", must_not_run)
    ui, _ = capture_ui()
    report = await demo.run_demo(step=True, output=tmp_path / "report.json", ui=ui)
    assert report["state"] == "cancelled" and not report["passed"] and not report["cases"]
