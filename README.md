# CedarBridge C5 MCP Toolkit

EECE 503P/798S: Agentic Systems, Fall 2026, American University of Beirut.

CedarBridge is a fictional student-project coaching business. Its assistant, Mira, uses the **OpenAI Agents SDK** to discover and invoke exactly **three FastMCP tools** over stdio. Facts come from a local JSON catalog; follow-up interests are stored in SQLite. C5 runs independently of the earlier [C3 project](https://github.com/Jiany-S/C3).

| Category | Tool | Responsibility |
|---|---|---|
| Data | `get_service_details(service_name)` | Read service facts without changing records |
| Action | `record_service_interest(name, email, service_name, notes, follow_up_requested)` | Save explicitly requested follow-up interest and return its committed ID |
| Orchestration | `register_verified_service_interest(name, email, service_name, notes, follow_up_requested)` | Verify the service, then conditionally save interest and return the actual sequence |

Inputs are typed; outputs use a Pydantic `ToolResult`. Failures have explicit outcomes. Repeated normalized email/service pairs return the existing ID without inserting or updating. Recording never books an appointment, sends email or takes payment.

## Submission documents

- [Research summary](docs/mcp_research_summary.md): 371 words, excluding title and references.
- [Reflection](docs/reflection.md): two paragraphs on boundaries, challenges and future work.
- [Architecture](docs/architecture.md) and [tool contracts](docs/tool_design.md).
- [Requirements and evidence](docs/compliance_report.md).
- [Submission handoff and video status](docs/submission.md).

Repository: [Jiany-S/C5](https://github.com/Jiany-S/C5), verified public on 2026-11-01. A screencast is recorded locally; its hosted sharing link is still pending. Recordings are delivered separately from source.

## Install

Python **3.11 on Windows** is the tested environment. Run these PowerShell commands from the C5 directory:

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements-lock.txt
.venv\Scripts\python.exe -m pip check
```

The lock reproduces the tested FastMCP 4.1.4, MCP Python SDK 2.3.0, OpenAI Agents SDK 0.24.0 and OpenAI SDK 3.41.0 environment. Direct runtime pins are in `requirements.txt`; `requirements-dev.txt` adds tests. The lock's pywin32 entry is Windows-only. On macOS/Linux replace `.venv\Scripts\python.exe` with `.venv/bin/python`; those platforms have not been tested here. No Node.js, browser, GPU or additional service is needed to run the project.

## Verify without an API key

```powershell
.venv\Scripts\python.exe agent_client.py --list-tools
.venv\Scripts\python.exe -m scripts.protocol_demo
.venv\Scripts\python.exe -m pytest -q
```

Discovery connects to a real FastMCP subprocess. The protocol demo calls all three tools and checks failures, consent and duplicates in a temporary store. It uses **no model**. Tests also use temporary stores. Scripted-model SDK tests are labeled separately from real OpenAI calls.

## Run the live agent

Create `.env` only if it does not exist, then edit it locally to set `OPENAI_API_KEY`:

```powershell
if (-not (Test-Path .env)) { Copy-Item .env.example .env }
.venv\Scripts\python.exe agent_client.py
```

An existing shell key takes precedence over C5's `.env`. The default model is `gpt-4.1-mini`, used in the saved live evidence. The host starts and closes the MCP server automatically; do not start another server terminal.

Try:

```text
What does Project Clarity cost, how long is it, and how is it delivered? I only want information.
```

| Chat command | Effect |
|---|---|
| `/help` | Explain the interface |
| `/examples` | Show three complete example requests |
| `/tools` | Discover the actual registered tools |
| `/records` | Inspect saved services and IDs, with contacts hidden |
| `/new` | Clear chat history while retaining saved interests |
| `/quit` | Close the session; `quit` and `exit` also work |

Actual MCP receipts show returned outcomes and IDs separately from Mira's model-generated answer. `/records` is a local operator command, not a fourth MCP tool. Use `--prompt "..."` for one request, `--data-dir runtime/my-demo` for an isolated store, `--schemas` for full discovered schemas, or `--trace` for raw MCP results and server events. Relative record paths start at the C5 directory.

## Demonstrate all three tools

```powershell
.venv\Scripts\python.exe -m scripts.live_demo --step
```

Press Enter to run each case or `q` to stop. The seven tested cases cover Data, Action, Orchestration, failed lookup, duplicates, information with contact details, and invalid email. Each run creates a fresh store and report under ignored `runtime/demo-.../`. Reports preserve partial failures and cancellations. Routing is model-selected; no `tool_choice` override or local-function bypass is used.

Inspect the directory printed by the demo:

```powershell
.venv\Scripts\python.exe -m scripts.inspect_records --data-dir runtime/demo-REPLACE_WITH_PRINTED_ID
```

The inspector opens SQLite read-only and hides contact details and notes. The [recording plan](docs/video_demo_plan.md) contains exact tested prompts and explanations. Its caption file is a draft, not subtitles aligned to the final recording.

## Validation evidence

- Ordinary suite: **49 passed, 1 skipped**. The skip is the opt-in paid API test.
- Saved real OpenAI run: **7/7 scenarios passed**, with actual MCP calls and two persisted records.
- Protocol demo: **7/7 cases passed** without a model or key.
- Research summary: **371 words**; reflection: **two paragraphs**.

See the [evidence index](evidence/README.md), [current validation](docs/submission_review.md), and [compliance matrix](docs/compliance_report.md). Earlier failed and intermediate reports remain unchanged under `evidence/history/` and are not counted as current passes. Model-answer checks are heuristics, reviewed alongside actual tool outcomes.

Set `RUN_LIVE_TESTS=1` with a configured key to enable the optional paid pytest case. Normal pytest does not make paid calls. The standalone live demo is recommended for a new evidence report.

## Scope and troubleshooting

- Install the lock if startup fails; `--list-tools` works without a key. The child uses `FASTMCP_CHECK_FOR_UPDATES=off` for the tested FastMCP version.
- Server stdout is reserved for MCP. Trace-mode business events use stderr. Check domain `status/code` as well as MCP `is_error`.
- Authentication, quota and network failures have safe recovery messages. Raw provider and storage exception bodies are not printed.
- Consent is asserted by a trusted local host, not authenticated identity proof. There is no booking calendar, email delivery, contact-ownership verification or automatic retention.
- The OpenAI model receives the conversation and necessary tool arguments. Cloud tracing is disabled; the server receives no OpenAI key. Use fictional names and example.com contacts in demonstrations.
- Runtime databases retain contact information locally. Keep stores, `.env`, environments and recordings outside Git and the source ZIP. Windows/Python 3.11 is validated; arbitrary adversarial prompts and other platforms are not claimed as tested.

## Source layout

```text
agent_client.py        Agents SDK host, MCP connection and CLI
mcp_server.py          Exactly three registered FastMCP tools
business.py            Typed results, catalog lookup and SQLite transaction
config.py              Shared project-relative record paths
terminal_ui.py         Chat presentation and actual MCP receipts
business_data/         Fictional read-only service catalog
scripts/               Protocol/live demos, inspector and source packaging
tests/                 Real MCP, scripted SDK, CLI and evidence checks
docs/                  Research, reflection, architecture and submission review
evidence/              Current evidence and labeled historical reports
```

Build the source ZIP with `.venv\Scripts\python.exe -m scripts.package_submission`. Its allowlist excludes secrets, databases, environments, caches, recordings and course materials.
