"""User-facing recovery, credential-free discovery and configuration consistency."""
import argparse
from io import StringIO
from types import SimpleNamespace

import pytest
from rich.console import Console

import agent_client
from config import ROOT, data_directory
from scripts.inspect_records import configured_directory
from terminal_ui import TerminalUI


def args(**changes):
    return argparse.Namespace(**(dict(list_tools=False, schemas=False, trace=False, prompt=None, data_dir=None) | changes))


def capture_ui():
    output = StringIO()
    return TerminalUI(Console(file=output, width=80, color_system=None)), output


def test_empty_one_shot_is_rejected_without_looping():
    with pytest.raises(argparse.ArgumentTypeError, match="must contain text"):
        agent_client.nonempty_prompt("   ")


async def test_missing_key_gives_specific_recovery_without_secret(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.setattr(agent_client, "load_dotenv", lambda *a, **k: None)
    with pytest.raises(agent_client.SetupError, match="--list-tools") as error:
        await agent_client.cli(args())
    assert "OPENAI_API_KEY" in str(error.value) and ".env.example" in str(error.value)


async def test_schemas_are_machine_readable_without_key(monkeypatch, capsys):
    import json
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.setattr(agent_client, "load_dotenv", lambda *a, **k: None)
    assert await agent_client.cli(args(schemas=True)) == 0
    tools = json.loads(capsys.readouterr().out)
    assert {tool["name"] for tool in tools} == agent_client.TOOL_NAMES


async def test_chat_commands_and_error_recovery_preserve_session(monkeypatch, tmp_path):
    monkeypatch.setenv("OPENAI_API_KEY", "synthetic-ui-test-key")
    prompts = iter(["/help", "/examples", "/tools", "/records", "/new", "/wrong", "first request", "second request", "/quit"])
    monkeypatch.setattr("builtins.input", lambda _: next(prompts))
    calls = []

    async def runner(agent, history, **kwargs):
        calls.append(history)
        if len(calls) == 1:
            raise RuntimeError("synthetic-private-provider-body")
        return SimpleNamespace(final_output="Recovered response.", to_input_list=lambda: history)

    monkeypatch.setattr(agent_client.Runner, "run", runner)
    ui, output = capture_ui()
    assert await agent_client.cli(args(data_dir=str(tmp_path)), ui=ui) == 0
    text = output.getvalue()
    assert "Recovered response" in text and "Session closed" in text
    assert "Unknown command" in text and "New conversation started" in text
    assert "Saved follow-up interests: 0" in text
    assert "synthetic-private-provider-body" not in text
    assert len(calls) == 2 and len(calls[-1]) == 1  # Failed history was not retained.
    assert not (tmp_path / "interests.sqlite3").exists()  # UI commands never invoke writes.


def test_inspector_uses_dotenv_and_project_relative_paths(monkeypatch, tmp_path):
    import scripts.inspect_records as inspector
    monkeypatch.delenv("CEDARBRIDGE_DATA_DIR", raising=False)
    monkeypatch.setattr(inspector, "dotenv_values", lambda _: {"CEDARBRIDGE_DATA_DIR":"runtime/configured"})
    monkeypatch.chdir(tmp_path)
    assert configured_directory() == ROOT / "runtime/configured"
    assert configured_directory("runtime/explicit") == ROOT / "runtime/explicit"
    monkeypatch.setenv("CEDARBRIDGE_DATA_DIR", "runtime/from-shell")
    assert configured_directory() == data_directory("runtime/from-shell")


def test_receipt_wraps_at_narrow_width_and_does_not_expose_contact():
    ui, output = capture_ui()
    ui.receipt({"status":"ok", "code":"interest_recorded", "created":True,
                "record_id":"12d7f2d0-a9c5-4217-b056-ef40f1e43833", "email":"private@example.com"})
    text = output.getvalue()
    assert "12d7f2d0-a9c5-4217-b056-ef40f1e43833" in text
    assert "private@example.com" not in text
    assert max(map(len, text.splitlines())) <= 80
