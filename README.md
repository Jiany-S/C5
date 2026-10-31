# CedarBridge C5 MCP Toolkit

EECE 503P/798S: Agentic Systems, Fall 2026, American University of Beirut. A standalone progression from the fictional [C3 CedarBridge concept](https://github.com/Jiany-S/C3), with no dependency on its application code.

Mira uses the **OpenAI Agents SDK** to discover and invoke exactly **three FastMCP tools** over a real stdio connection. The business facts are local; OpenAI is the only API needed for the agent demonstration.

| Category | Tool | What it does |
|---|---|---|
| Data | `get_service_details(service_name)` | Reads deterministic published service facts |
| Action | `record_service_interest(name, email, service_name, notes, follow_up_requested)` | Saves explicit follow-up interest in SQLite and returns the committed record ID |
| Orchestration | `register_verified_service_interest(name, email, service_name, notes, follow_up_requested)` | Runs lookup, then conditionally records interest, returning the actual sequence |

All inputs are typed; the output is a Pydantic `ToolResult`. Recording never books an appointment, sends an email, or takes payment. Duplicate normalized email/service pairs return their existing ID without inserting or updating. See [tool contracts](docs/tool_design.md) and [architecture](docs/architecture.md).

## Install from a clean environment

Python **3.11** was tested on Windows. Run commands from this directory. There is no need to start a separate server terminal: the client owns the subprocess.

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements-lock.txt
.venv\Scripts\python.exe -m pip check
```

The complete lock includes development dependencies and a Windows-only marker for pywin32. Alternatively, `requirements.txt` pins direct runtime packages and `requirements-dev.txt` adds tests. FastMCP 4.1.4, MCP Python SDK 2.3.0, Agents SDK 0.24.0 and OpenAI SDK 3.41.0 were current available releases checked on 2026-10-30. Pins reproduce the tested APIs rather than silently adopting future breaking changes.

On macOS/Linux use `.venv/bin/python` in place of `.venv\Scripts\python.exe`. Those systems have not been executed in this submission's validation. No notebook, Node.js, browser, GPU or extra service is required.

## Verify MCP without credentials

```powershell
.venv\Scripts\python.exe agent_client.py --list-tools
.venv\Scripts\python.exe -m scripts.protocol_demo
.venv\Scripts\python.exe -m pytest -q
```

`--list-tools` shows a concise table of the actual discovered tools and categories. Use `--schemas` for complete machine-readable JSON schemas, or `--trace` to include raw result JSON and server capability events. The protocol demo starts a real server and calls all three tools, including failure, duplicate and no-consent cases, in an automatically removed temporary store. It does **not** use a model and is labeled accordingly. The pytest suite also uses temporary stores.

## Configure the live OpenAI agent

Create `.env` from `.env.example` if it does not already exist, then fill `OPENAI_API_KEY` locally. Edit an existing `.env` without overwriting its contents. Never paste a key into a chat prompt or Git. The host loads only C5's `.env`, never another project's file. An existing shell `OPENAI_API_KEY` takes precedence. `OPENAI_MODEL` defaults to `gpt-4.1-mini`, which was used for the saved real tests.

```powershell
if (-not (Test-Path .env)) { Copy-Item .env.example .env }
# Edit .env locally to configure the key. Then:
.venv\Scripts\python.exe agent_client.py
```

Interactive prompt example:

```text
What does Project Clarity cost, how long is it, and how is it delivered? I only want information.
```

The welcome panel shows the model, record directory and available commands. Normal output separates actual MCP receipts from Mira's model-generated answer. A receipt always shows the returned record ID, even if model wording varies.

| Chat command | Effect |
|---|---|
| `/help` | Show how to use the assistant |
| `/examples` | Show three copy-paste requests |
| `/tools` | Show actual server-discovered tools |
| `/records` | Inspect saved IDs and services; contacts remain hidden |
| `/new` | Clear conversation history; saved interests remain |
| `/quit` | Close the connection; `quit` and `exit` also work |

One request can run with `--prompt "..."`; blank one-shot prompts are rejected. `--data-dir runtime/my-demo` selects a separate local store. All relative data paths, including inspector paths, start at the C5 project directory. Missing-key errors give setup instructions; an individual chat error allows recovery without closing the session. `/records` is a local operator command, not a fourth MCP tool available to the agent.

## Live demonstration and evidence

```powershell
.venv\Scripts\python.exe -m scripts.live_demo
# For the 5–7-minute recording, pause before every case:
.venv\Scripts\python.exe -m scripts.live_demo --step
```

Each run creates a fresh ignored `runtime/demo-...` directory, prints it, and sends the seven tested prompts to the real model. It prints actual client boundary events, server capability outcomes, the model's answer, and read-only persistence proof. Model routing is automatic; there is no `tool_choice` override or local function bypass. The retry case may safely use either writing interface. The dedicated Action and Orchestration cases each require the respective tool.

The step view labels progress as 1/7 through 7/7. Press Enter to run a case or `q` to stop; EOF also stops safely. Compact receipts show the actual outcome and orchestration sequence. Add `--trace` for full JSON and server-side event logs.

By default each new run saves `runtime/demo-.../live_report.json`, preserving the supplied submission evidence. Reports are saved atomically before execution, after each case and on failure/cancellation. An interrupted run is marked incomplete and cannot inherit an earlier pass. To intentionally create a new submission report, use `--output evidence/my-reviewed-run.json`. Automated prose checks are heuristics; review final model answers before recording.

Results from final validation:

- **49 passed, 1 skipped** in ordinary pytest: 29 protocol tests, 6 scripted-model SDK tests, 6 CLI/configuration tests and 8 evidence/evaluation tests passed. The opt-in paid API test was skipped there.
- **7/7 real OpenAI scenarios passed** separately: Data, Action, Orchestration, failed lookup, duplicate, information with contact details, and invalid email. Two records were created; all later cases retained the count of two.
- **7/7 protocol-demo cases passed** with no model or key.
- Research main summary: **371 whitespace-delimited words**, within 300–400. Reflection: **2 paragraphs**.

Inspect [final live results](evidence/live_agent.json), [actual discovery and protocol calls](evidence/protocol.json), [pytest XML](evidence/pytest.xml), and the [strict compliance report](docs/compliance_report.md). Initial live reports are intentionally preserved and marked `passed=false`; they document limitations found during refinement. The test fixture's scripted model is explicitly labeled and is not evidence of real model selection.

The [independent subagent review](docs/independent_review.md) rated the revised technical/written work at approximately **95/100 unofficially**, while correctly keeping the full submission incomplete without its video and links. Its findings led to stronger validation, consistent inspector configuration, more reliable evidence and a clearer CLI. [Interface review](docs/interface_review.md) includes narrow-terminal previews and tested user flows.

The [extracted-archive check](evidence/archive_reproduction.json) also passed discovery from an outside working directory and all seven protocol cases using an extracted source copy with the same tested dependency environment. It does not claim a second dependency installation.

To run the paid live scenario as part of pytest, configure your key and set `RUN_LIVE_TESTS=1` before running pytest. Normal tests never incur API charges. The standalone live demo is the recommended evidence-producing command.

## Inspect saved records

Use the directory printed by the live demo:

```powershell
.venv\Scripts\python.exe -m scripts.inspect_records --data-dir runtime/demo-REPLACE_WITH_PRINTED_ID
```

The inspection script uses SQLite read-only mode and shows IDs, services, timestamps and consent flags. It hides contact details and notes. Runtime SQLite files contain customer-supplied data and are ignored by Git. For demonstrations use fictional names and example.com emails only. The operator controls local file access and retention.

## Recording and submission

Follow [the exact 6-minute recording plan](docs/video_demo_plan.md), including the successfully tested prompts. Silent recording with readable captions is supported by the plan; the PDF specifies a screencast but does not explicitly require narration. This is an interpretation of the wording, not an instructor's approval of a particular format.

The code, research, reflection and execution evidence are prepared. **The actual video and published repository/video links remain outstanding.** No video is fabricated and no repository has been published. Read [submission steps](docs/submission.md) before uploading anything. The course PDFs/notebooks are referenced, not redistributed.

## Troubleshooting and limits

- A server disconnect at startup usually means wrong dependencies or working directory. Install the pins and use the supplied client. Current FastMCP's `FASTMCP_CHECK_FOR_UPDATES` takes `off`, not `false`; the client sets it correctly.
- API authentication, quota, network or model-access problems do not affect credential-free MCP tests. Verify the local key and account access; the CLI suppresses provider exception bodies to avoid leaking credentials or request data.
- The server's stdout is reserved for MCP. With `--trace`, business logs go to stderr and the client adds raw JSON. Compact mode displays client receipts for actual calls. Do not add ordinary `print()` calls inside server functions.
- Unknown services and invalid contacts return structured failures. Schema violations return MCP errors. Inspect `status/code` as well as `is_error`; domain errors are valid structured results.
- Repeating an email/service does not update notes. One outstanding interest per pair is a deliberate scope limit. There is no booking calendar, email, authentication, automatic retention or contact-ownership verification.
- Consent is asserted by a trusted local host; a malicious MCP client can lie about it. Model instructions do not guarantee perfect routing or prose under arbitrary adversarial inputs. The saved tests show observed behavior for specified cases, not a universal guarantee.
- Windows/Python 3.11 is tested. Other operating systems and Python versions are not claimed as executed.

## Project contents

`mcp_server.py`: three registered tools; `business.py`: typed contracts, catalog and transactions; `agent_client.py`: actual Agents SDK MCP host; `terminal_ui.py`: readable receipts and chat presentation; `config.py`: consistent local paths; `scripts/`: protocol/live demo, read-only inspector, interface preview and packaging; `tests/`: protocol, scripted-model SDK, CLI recovery and evidence checks; `docs/`: research, contracts, architecture, reflection, reviews and recording plan; `evidence/`: synthetic execution reports and source provenance.
