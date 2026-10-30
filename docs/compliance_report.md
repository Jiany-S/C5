# Strict final review

Reviewed 2026-10-30 after re-reading all three pages of the authoritative assignment. This is an assistant's self-assessment, not an independent human review or a professor-issued grade. Published requirements are separated from the additional engineering checks requested by the user.

**Outcome:** the local implementation, written deliverables, real MCP verification and live agent demonstration are prepared. The overall submission is **PARTIAL** until the actual 5–7-minute video is recorded, uploaded and submitted with a published accessible code repository. A plan or JSON log does not substitute for the video.

## Published assignment requirements

| Requirement | Exact implementation location | Evidence/test | Status | Correction / next action |
|---|---|---|---|---|
| Read Hugging Face article | `docs/sources_review.md`; `docs/mcp_research_summary.md` | Public introduction and linked expansion reviewed; article scope disclosed | PASS | None |
| Inspect existing MCP server | `docs/mcp_research_summary.md`, reference 3 | Fetch source pinned to `fb31aa5ad2852ac2cb272fc7de7225547e1ed870`; actual handlers inspected | PASS | None |
| Summary 300–400 words | `docs/mcp_research_summary.md`, marked main body | 371 whitespace-delimited words; `evidence/security_audit.json` | PASS | Keep references outside counted body |
| Explain Host/Client/Server and MCP concepts | Summary paragraphs 1–3; `docs/architecture.md` | Describes discovery, typed definitions, invocation, outputs and host execution | PASS | None |
| Critique server using class principles | Summary paragraphs 4–5 | Focus, parameter bounds, errors, output modes, changing external data and untrusted content | PASS | None |
| Coherent original/inspired theme | `business_data/services.json` | CedarBridge facts match read-only C3 summary; no C3 application dependency | PASS | None |
| Exactly three distinct tools | `mcp_server.py` three `@mcp.tool` definitions | `test_start_connect_and_exact_schemas`; `evidence/protocol.json` actual discovery | PASS | Do not add helper decorators |
| One Data tool without state changes | `mcp_server.py:get_service_details`; `business.py:lookup_service` | `test_known_data_is_read_only`, all 3 services, no store creation/catalog changes | PASS | None |
| One Action tool with a real effect | `mcp_server.py:record_service_interest`; `business.py:record_interest` | `test_action_persists_and_duplicate_is_stable`; live record ID and row count | PASS | None |
| One Orchestration tool coordinates the other capabilities | `business.py:register_verified_interest` | `test_orchestration_real_lookup_then_action`; actual `steps`, server events and persisted row | PASS | Shared business functions are internal calls, not claimed as nested MCP calls |
| Clear descriptions, typed inputs and output | Decorated signatures; `business.py:Service`, `Step`, `ToolResult`; `docs/tool_design.md` | Discovered input/output schemas asserted over MCP | PASS | None |
| Focused single responsibility | `docs/tool_design.md`, tool table and boundary rationale | Separate read, write, verify-then-write contracts | PASS | Retry routing overlap is documented; do not portray routing as perfectly deterministic |
| Predictable failure for every tool | Business codes and FastMCP validation | Unknown Data lookup; invalid Action contact/storage; Orchestration lookup failure/consent gate | PASS | None |
| FastMCP server | `mcp_server.py`, `FastMCP(...)` and `run(transport="stdio")` | Actual server process used in all protocol and live tests | PASS | None |
| OpenAI Agents SDK host/client | `agent_client.py:make_server`, `make_agent`, `cli` | `Agent(mcp_servers=[server])`, `Runner.run`, actual SDK connection; no local function tools | PASS | None |
| Agent routes requests through MCP | `ObservableMCPServer.call_tool` awaits SDK super-method | Final live Data/Action/Orchestration cases selected distinct tools and returned actual results | PASS | None |
| Functional tests including failures | `tests/test_protocol.py`, `tests/test_agent.py`, `scripts/protocol_demo.py` | 33 passed, 1 opt-in live test skipped in ordinary suite; 7/7 separate real live cases | PASS | Skipped ordinary live test is not presented as an API execution |
| Configuration and README | `README.md`, `.env.example`, requirements files | Fresh isolated Python 3.11 installation; `pip check` passed | PASS | Windows tested; other OSes not claimed as executed |
| Written summary and source deliverables | Standalone C5 source, docs and ZIP | File inventory, ZIP integrity and extracted-copy MCP discovery/protocol verification | PASS | Rebuild ZIP after adding real submission links |
| Reflection, 1–2 paragraphs | `docs/reflection.md` | Two paragraphs; real observed decisions/challenges and next steps | PASS | Student should review and adapt to their own understanding |
| 5–7-minute screencast introduces tools/categories | `docs/video_demo_plan.md`, `docs/demo_captions.srt` | Detailed 6:20 plan; final live prompts verified | PARTIAL | Record actual video |
| Video shows full live round trips | Live demo command and saved execution evidence | All required round trips run successfully, but no recording exists | PARTIAL | Capture actual execution, inspect readability and duration |
| Video explains challenges and solutions | Recording plan 5:20–6:00; reflection | Real startup setting, SQLite handle issue, retry/routing and result wording observed | PARTIAL | Include this explanation in the recording |
| Repository and video links shared in submission | `docs/submission.md` | Explicit pending entries; no remote or upload fabricated | PARTIAL | Obtain publication approval, publish, record/upload, verify access and submit links |

## Additional engineering checks requested by the user

| Check | Exact location / evidence | Status | Correction / limit |
|---|---|---|---|
| Review notes, lecture, safety deck and 7 tutorials | `docs/sources_review.md`; `evidence/materials_manifest.json` | PASS | Source PDFs/notebooks deliberately not bundled |
| Requirements checklist created before code | `docs/requirements_checklist.md` | PASS | Manual video/publication items remain unchecked |
| Current compatible APIs verified | `docs/sources_review.md`; requirements lock; final real execution | PASS | Pins describe the tested date, not future latest releases |
| Separate standalone C5, C3/C4 untouched | New C5 `.git`; C3/C4 final `git status --short` empty | PASS | No C6 work performed |
| Async lifecycle and subprocess cleanup | `make_server` context; `test_connections_close_on_exception_and_release_store` | PASS | Explicit SQLite closure fixes the observed Windows leak |
| No unnecessary external APIs | Local JSON + SQLite; only host makes OpenAI calls | PASS | Live agent still requires OpenAI access |
| No API credential in source or child configuration | `evidence/security_audit.json`; explicit allowlist in `make_server` | PASS | Exact authorized key absent from deliverable files; no real `.env` in C5 |
| Persistent duplicate safety across concurrent processes | `test_concurrent_servers_and_restart_deduplicate` | PASS | One outstanding interest per normalized email/service; no update semantics |
| Meaningful temporary-store testing | `tests/conftest.py`; protocol demo temporary directory | PASS | Demo runtime stores are synthetic and ignored by Git |
| Cleanliness and package audit | `.gitignore`; `scripts/package_submission.py`; security evidence | PASS | No environments, caches, runtime databases or source course materials in submission |
| Paid model calls labeled separately from scripted responses | `tests/test_agent.py`; live report execution tag | PASS | Scripted tests verify plumbing, not genuine language reasoning |
| Tested video prompts and silent-caption option | `scripts/demo_cases.py`; final live report; recording plan | PASS | Narration not explicitly required by PDF; captions still need timing/readability review |
| Non-Windows environment execution | README portability notes | NOT TESTED | Optional future verification; Windows/Python 3.11 is the tested target |
| Arbitrary adversarial prompts / authenticated consent | Architecture limits | NOT TESTED | Server verifies Boolean intent, not user identity; do not expose publicly as a production service |

## Requested minimum testing matrix

| # | Required behavior | Exact test/evidence | Status |
|---|---|---|---|
| 1 | Server starts | `test_start_connect_and_exact_schemas` | PASS |
| 2 | Client connects | Same test and every subprocess fixture | PASS |
| 3 | Exactly three tools | Same test; `evidence/protocol.json:tools` | PASS |
| 4 | Correct names, descriptions and schemas | Same test checks categories, required fields, types, descriptions, output schema | PASS |
| 5 | Correct known Data results | `test_known_data_is_read_only`, 3 services | PASS |
| 6 | Unknown Data service | `test_unknown_service_and_recovery` | PASS |
| 7 | Genuine persistence | `test_action_persists_and_duplicate_is_stable`; direct SQLite row comparison | PASS |
| 8 | Invalid emails / required fields rejected | Domain, schema and missing-field parameterized tests | PASS |
| 9 | Orchestration performs lookup then action | `test_orchestration_real_lookup_then_action`; ordered steps and saved UUID | PASS |
| 10 | Failed lookup prevents write | `test_failed_lookup_stops_action`; directory not created | PASS |
| 11 | Agent invokes each through MCP | 3 scripted SDK cases plus 3 real live categories | PASS |
| 12 | Agent correctly uses returned facts, IDs and failures | Scripted result forwarding checks and final live cases/answers | PASS for specified cases |
| 13 | Information-only question does not write | Data read-only tests; live `data` and `information_with_contact` | PASS |
| 14 | Repeated requests safe | Concurrent/restart test plus live `repeat`, same ID and row count | PASS |
| 15 | Safe errors without credential exposure | Storage failure/recovery test, masked framework errors, host safe error handler and exact-key audit | PASS within tested local scope |

## Evidence interpretation and corrections made

`evidence/pytest.xml` contains the final 33 passed / 1 skipped run. Its hostname attribute was removed for privacy; counts and test results were not changed. The skip is the explicitly opt-in paid test. `evidence/live_agent.json` separately records a real `gpt-4.1-mini` run with seven passed scenarios. `evidence/protocol.json` records seven real MCP calls without a model and successful connection closure. Initial live JSON reports remain available and are not counted as final passes.

Early runs exposed a wrong FastMCP environment value, a test helper's `name` collision, and an unclosed SQLite handle on Windows. The first two were corrected; explicit `closing(...)` and a regression test resolved the handle issue. Early live responses overstated the staff response target or omitted the duplicate UUID. Instructions now require bounded wording, and the repeat prompt explicitly requests the ID. Repeated requests sometimes select orchestration even when the shorter Action route would suffice. That route is semantically safe, so the retry evaluation accepts either while requiring the same existing ID and unchanged count; it does not relax the dedicated tool-category scenarios.

## Strict academic assessment

The implementation is strong for this assignment: real interoperable transport, minimal local dependencies beyond the required frameworks, clear business boundaries, meaningful concurrency/failure tests, traceable research and honest evidence. The principal design cost is overlap between recording and verified recording. Explaining that tradeoff is preferable to claiming perfect model routing. The local Boolean consent gate and conservative email syntax are appropriate demonstration constraints, but they are not production authorization or identity verification.

I would assess the **technical and written work as high quality**, without inventing numerical weights or a professor's rubric. I would **not mark the full assignment complete or estimate a final course grade** before seeing the mandatory video and accessible submission links. Those deliverables remain substantive outstanding requirements.
