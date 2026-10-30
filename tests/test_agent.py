"""SCRIPTED MODEL tests: real Runner + real MCP, no OpenAI model/network calls."""
import json

import pytest
from agents import ModelResponse, Runner, Usage
from agents.models.interface import Model
from openai.types.responses import ResponseFunctionToolCall, ResponseOutputMessage, ResponseOutputText

from agent_client import TOOL_NAMES, make_agent
from tests.test_protocol import LEAD, rows


class ScriptedModel(Model):
    """Issue a supplied call, then build an answer from the real returned payload.

    This tests SDK plumbing and result forwarding, not language-model reasoning.
    """
    def __init__(self, tool_name, arguments):
        self.tool_name = tool_name
        self.arguments = arguments
        self.calls = 0
        self.received_result = None

    async def get_response(self, system_instructions, input, model_settings, tools, **kwargs):
        assert {t.name for t in tools} == TOOL_NAMES
        self.calls += 1
        if self.calls == 1:
            output = [ResponseFunctionToolCall(type="function_call", name=self.tool_name,
                      arguments=json.dumps(self.arguments), call_id="scripted-call-1")]
        else:
            outputs = [i for i in input if isinstance(i, dict) and i.get("type") == "function_call_output"]
            assert outputs and outputs[-1]["call_id"] == "scripted-call-1"
            value = outputs[-1]["output"]
            if isinstance(value, list):
                value = "\n".join(i["text"] for i in value if i.get("type") in {"text","input_text"})
            self.received_result = json.loads(value)
            payload = self.received_result
            if payload["code"] == "service_found":
                text = f"{payload['service']['name']}: USD {payload['service']['price_usd']}."
            elif payload["record_id"]:
                text = f"{payload['code']}: local follow-up record {payload['record_id']}. No appointment booked or email sent."
            else:
                text = f"{payload['code']}: no record saved."
            output = [ResponseOutputMessage(id="scripted-message", type="message", role="assistant", status="completed",
                      content=[ResponseOutputText(type="output_text", text=text, annotations=[])])]
        return ModelResponse(output=output, usage=Usage(), response_id=None)

    async def stream_response(self, *args, **kwargs):
        raise NotImplementedError("Scripted model tests use non-streaming Runner.run.")
        yield  # Make this an async iterator, matching the SDK's abstract interface.


@pytest.mark.parametrize("tool_name", sorted(TOOL_NAMES))
async def test_scripted_sdk_invokes_each_discovered_tool(server, tmp_path, tool_name):
    args = {"service_name":"Project Clarity"} if tool_name == "get_service_details" else LEAD
    model = ScriptedModel(tool_name, args)
    result = await Runner.run(make_agent(server, model), "SCRIPTED MODEL transport test", max_turns=3)
    assert len(server.events) == 1 and server.events[0]["tool"] == tool_name
    assert model.calls == 2
    assert model.received_result == server.events[0]["result"]
    if tool_name == "get_service_details":
        assert "USD 15" in result.final_output
        assert not rows(tmp_path / "records")
    else:
        assert rows(tmp_path / "records")[0][0] in result.final_output


@pytest.mark.parametrize("args,code", [
    (LEAD | {"service_name":"Unknown"}, "unknown_service"),
    (LEAD | {"follow_up_requested":False}, "consent_required"),
    (LEAD | {"email":"broken"}, "invalid_input"),
])
async def test_scripted_sdk_receives_failure_without_false_success(server, tmp_path, args, code):
    model = ScriptedModel("register_verified_service_interest", args)
    result = await Runner.run(make_agent(server, model), "SCRIPTED MODEL failure test", max_turns=3)
    assert model.received_result["code"] == code
    assert result.final_output == f"{code}: no record saved."
    assert not rows(tmp_path / "records")


@pytest.mark.live
async def test_real_openai_agent_when_explicitly_enabled():
    import os
    from scripts.live_demo import run_demo
    if os.getenv("RUN_LIVE_TESTS") != "1":
        pytest.skip("Real paid API test is opt-in: RUN_LIVE_TESTS=1; evidence/live_agent.json records separate execution.")
    report = await run_demo()
    assert report["passed"]
